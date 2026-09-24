param(
  [Parameter(Mandatory = $true)]
  [string]$Root,
  [switch]$SkipDbmlCompile
)

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path
$errors = [System.Collections.Generic.List[string]]::new()

function Add-Error([string]$message) {
  $script:errors.Add($message)
}

foreach ($required in @('FIGMA.md', 'CONTEXT.md', 'ASSUMPTIONS.md', 'coverage-report.md', 'schema.dbml', 'uc', 'api')) {
  if (-not (Test-Path -LiteralPath (Join-Path $rootPath $required))) {
    Add-Error "Missing required artifact: $required"
  }
}

$ucDir = Join-Path $rootPath 'uc'
$apiDir = Join-Path $rootPath 'api'
$ucFiles = if (Test-Path $ucDir) { @(Get-ChildItem $ucDir -Filter '*.md' | Where-Object Name -Match '^uc-\d{2}-[a-z0-9-]+\.md$') } else { @() }
$apiFiles = if (Test-Path $apiDir) { @(Get-ChildItem $apiDir -Filter 'api-*.md' | Where-Object Name -NotMatch '^README\.md$|^common-contract\.md$') } else { @() }

if ($ucFiles.Count -lt 18 -or $ucFiles.Count -gt 20) {
  Add-Error "Expected 18 to 20 individual UC files; found $($ucFiles.Count)."
}
if ($apiFiles.Count -eq 0) { Add-Error 'No individual API files found.' }

if (Test-Path $apiDir) {
  foreach ($apiDocument in Get-ChildItem $apiDir -Filter '*.md' -File) {
    $apiDocumentText = Get-Content -Encoding UTF8 -Raw -LiteralPath $apiDocument.FullName
    if ($apiDocumentText -match '(?i)```(?:plantuml|ocl)|\bBR-API-[A-Z0-9-]+\b') {
      Add-Error "$($apiDocument.Name): the API directory must not contain UML, OCL, or API rule identifiers."
    }
    if ($apiDocumentText -match '(?m)^\s*\|') {
      Add-Error "$($apiDocument.Name): API documentation must use a sequential layout without Markdown tables."
    }
  }
}

$allRuleIds = [System.Collections.Generic.List[string]]::new()
$allBehaviorIds = [System.Collections.Generic.List[string]]::new()
$allFlowActivityCount = 0
$apiDefinitions = [System.Collections.Generic.HashSet[string]]::new()
$apiReferences = [System.Collections.Generic.HashSet[string]]::new()
$ucDefinitions = [System.Collections.Generic.HashSet[string]]::new()
$apiRelatedUcs = @{}
$ucRelatedApis = @{}

foreach ($file in @($ucFiles) + @($apiFiles)) {
  $text = Get-Content -Encoding UTF8 -Raw -LiteralPath $file.FullName
  $expectedHeading = if ($file.Directory.Name -eq 'uc') { '^# UC-\d{2} — ' } else { '^# API-[A-Z0-9-]+ — ' }
  if (([regex]::Matches($text, "(?m)$expectedHeading")).Count -ne 1) {
    Add-Error "$($file.Name): expected exactly one matching top-level heading."
  }

  if (([regex]::Matches($text, '(?m)^```')).Count % 2 -ne 0) {
    Add-Error "$($file.Name): unbalanced Markdown fences."
  }

  $ruleBlocks = [regex]::Matches($text, '(?ms)```ocl\r?\n(.*?)\r?\n```') |
    Where-Object { $_.Groups[1].Value -match '(?m)^-- BR-' }

  foreach ($block in $ruleBlocks) {
    $body = $block.Groups[1].Value
    $ids = [regex]::Matches($body, '(?m)^-- (BR-[A-Z0-9-]+)\r?$')
    $contexts = [regex]::Matches($body, '(?m)^context ')
    $constraints = [regex]::Matches($body, '(?m)^(pre|post|inv) ')
    if ($ids.Count -ne 1 -or $contexts.Count -ne 1 -or $constraints.Count -ne 1) {
      Add-Error "$($file.Name): every OCL rule block needs one ID, context, and constraint."
    } elseif (-not $allRuleIds.Contains($ids[0].Groups[1].Value)) {
      $allRuleIds.Add($ids[0].Groups[1].Value)
    } else {
      Add-Error "Duplicate rule ID: $($ids[0].Groups[1].Value)"
    }
  }

  $lines = $text -split '\r?\n'
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^#{2,3} Business Rules') {
      $level = ([regex]::Match($lines[$i], '^#+')).Value.Length
      $insideOcl = $false
      for ($j = $i + 1; $j -lt $lines.Count; $j++) {
        $heading = [regex]::Match($lines[$j], '^(#+) ')
        if ($heading.Success -and $heading.Groups[1].Value.Length -le $level) { break }
        if ($lines[$j] -eq '```ocl') { $insideOcl = $true; continue }
        if ($lines[$j] -eq '```' -and $insideOcl) { $insideOcl = $false; continue }
        if (-not $insideOcl -and $lines[$j].Trim().Length -gt 0) {
          Add-Error "$($file.Name): non-OCL content inside Business Rules section."
          break
        }
      }
    }
  }

  if ($file.Directory.Name -eq 'uc') {
    $ucHeading = [regex]::Match($text, '(?m)^# UC-(\d{2}) — ')
    $ucNumber = if ($ucHeading.Success) { $ucHeading.Groups[1].Value } else { '' }
    if ($ucHeading.Success) { [void]$ucDefinitions.Add("UC-$ucNumber") }
    $codedItemSections = @(
      @{ Heading = 'Trigger'; Prefix = 'TRG'; Marker = 'plain' },
      @{ Heading = 'Preconditions'; Prefix = 'PRE'; Marker = 'bullet' },
      @{ Heading = 'Postconditions'; Prefix = 'POST'; Marker = 'bullet' }
    )

    foreach ($section in $codedItemSections) {
      $escapedHeading = [regex]::Escape($section.Heading)
      $sectionMatch = [regex]::Match(
        $text,
        "(?ms)^### $escapedHeading\s*\r?\n(.*?)(?=^### |\z)"
      )
      if (-not $sectionMatch.Success) {
        Add-Error "$($file.Name): missing $($section.Heading) section."
        continue
      }

      $bodyLines = @($sectionMatch.Groups[1].Value -split '\r?\n' |
        Where-Object { $_.Trim().Length -gt 0 })
      if ($bodyLines.Count -eq 0) {
        Add-Error "$($file.Name): $($section.Heading) must contain at least one coded item."
        continue
      }

      $prefix = $section.Prefix
      $markerPattern = switch ($section.Marker) {
        'plain' { '^\*\*' }
        'bullet' { '^- \*\*' }
        'number' { '^\d+\. \*\*' }
      }
      $idPattern = "$markerPattern($prefix-UC-$ucNumber-(\d{2}))\*\* — .+$"
      $sectionSequences = [System.Collections.Generic.List[int]]::new()

      foreach ($line in $bodyLines) {
        $itemMatch = [regex]::Match($line, $idPattern)
        if (-not $itemMatch.Success) {
          Add-Error "$($file.Name): malformed or uncoded item in $($section.Heading): $line"
          continue
        }
        $behaviorId = $itemMatch.Groups[1].Value
        $sequence = [int]$itemMatch.Groups[2].Value
        $sectionSequences.Add($sequence)
        if ($allBehaviorIds.Contains($behaviorId)) {
          Add-Error "Duplicate behavior ID: $behaviorId"
        } else {
          $allBehaviorIds.Add($behaviorId)
        }
      }

      for ($sequenceIndex = 0; $sequenceIndex -lt $sectionSequences.Count; $sequenceIndex++) {
        $expectedSequence = $sequenceIndex + 1
        if ($sectionSequences[$sequenceIndex] -ne $expectedSequence) {
          Add-Error "$($file.Name): $($section.Heading) IDs must be gap-free from 01."
          break
        }
      }
    }

    $basicFlowHeadingCount = [regex]::Matches($text, '(?m)^### Basic Flow\s*$').Count
    if ($basicFlowHeadingCount -ne 1) {
      Add-Error "$($file.Name): expected exactly one Basic Flow section."
    }
    $basicFlowMatch = [regex]::Match(
      $text,
      '(?ms)^### Basic Flow\s*\r?\n(.*?)(?=^### |\z)'
    )
    if (-not $basicFlowMatch.Success) {
      Add-Error "$($file.Name): missing Basic Flow section."
    } else {
      $basicFlowLines = @($basicFlowMatch.Groups[1].Value -split '\r?\n' |
        Where-Object { $_.Trim().Length -gt 0 })
      if ($basicFlowLines.Count -eq 0) {
        Add-Error "$($file.Name): Basic Flow must contain numbered activities."
      }
      for ($basicIndex = 0; $basicIndex -lt $basicFlowLines.Count; $basicIndex++) {
        $activityMatch = [regex]::Match($basicFlowLines[$basicIndex], '^(\d+)\. (.+)$')
        if (-not $activityMatch.Success) {
          Add-Error "$($file.Name): malformed Basic Flow activity: $($basicFlowLines[$basicIndex])"
          continue
        }
        if ([int]$activityMatch.Groups[1].Value -ne $basicIndex + 1) {
          Add-Error "$($file.Name): Basic Flow activities must be gap-free from 1."
          break
        }
        if ($activityMatch.Groups[2].Value -match '\*\*(BF|AF|EF)-UC-|\b(BF|AF|EF)-UC-') {
          Add-Error "$($file.Name): Basic Flow activities must not have identifiers."
        }
        $allFlowActivityCount++
      }
    }

    $branchSections = @(
      @{ Heading = 'Alternative Flows'; Prefix = 'AF' },
      @{ Heading = 'Exception Flows'; Prefix = 'EF' }
    )

    foreach ($section in $branchSections) {
      $escapedHeading = [regex]::Escape($section.Heading)
      $sectionMatch = [regex]::Match(
        $text,
        "(?ms)^### $escapedHeading\s*\r?\n(.*?)(?=^### |\z)"
      )
      if (-not $sectionMatch.Success) {
        Add-Error "$($file.Name): missing $($section.Heading) section."
        continue
      }

      $bodyLines = @($sectionMatch.Groups[1].Value -split '\r?\n' |
        Where-Object { $_.Trim().Length -gt 0 })
      $prefix = $section.Prefix
      $flowSequences = [System.Collections.Generic.List[int]]::new()
      $currentFlowId = $null
      $currentActivityCount = 0

      foreach ($line in $bodyLines) {
        $headingMatch = [regex]::Match(
          $line,
          "^#### ($prefix-UC-$ucNumber-(\d{2}))$"
        )
        if ($headingMatch.Success) {
          if ($currentFlowId -ne $null -and $currentActivityCount -eq 0) {
            Add-Error "$($file.Name): $currentFlowId must contain at least one numbered activity."
          }
          $currentFlowId = $headingMatch.Groups[1].Value
          $currentActivityCount = 0
          $flowSequences.Add([int]$headingMatch.Groups[2].Value)
          if ($allBehaviorIds.Contains($currentFlowId)) {
            Add-Error "Duplicate behavior ID: $currentFlowId"
          } else {
            $allBehaviorIds.Add($currentFlowId)
          }
          continue
        }

        $activityMatch = [regex]::Match($line, '^(\d+)\. (.+)$')
        if (-not $activityMatch.Success -or $currentFlowId -eq $null) {
          Add-Error "$($file.Name): malformed branch flow content in $($section.Heading): $line"
          continue
        }
        $currentActivityCount++
        if ([int]$activityMatch.Groups[1].Value -ne $currentActivityCount) {
          Add-Error "$($file.Name): activities under $currentFlowId must be gap-free from 1."
        }
        if ($activityMatch.Groups[2].Value -match '\*\*(AF|EF)-UC-|\b(AF|EF)-UC-') {
          Add-Error "$($file.Name): activities under $currentFlowId must not have individual flow identifiers."
        }
        $allFlowActivityCount++
      }

      if ($currentFlowId -eq $null) {
        Add-Error "$($file.Name): $($section.Heading) must contain at least one coded flow."
      } elseif ($currentActivityCount -eq 0) {
        Add-Error "$($file.Name): $currentFlowId must contain at least one numbered activity."
      }

      for ($flowIndex = 0; $flowIndex -lt $flowSequences.Count; $flowIndex++) {
        if ($flowSequences[$flowIndex] -ne $flowIndex + 1) {
          Add-Error "$($file.Name): $($section.Heading) IDs must be gap-free from 01."
          break
        }
      }
    }

    $interactionText = [regex]::Match(
      $text,
      '(?ms)^### Trigger\s+(.*?)(?=^### UML Model)'
    ).Groups[1].Value
    $policyLeakPattern = '(?i)\bBusiness Rules?\b|\bBR-[A-Z0-9-]+\b|>=|<=|allInstances|matches\(|isUnique|Set\{|::|\b(predicate|threshold|formula|eligibility|authorization|ownership|normalization|ordering|calculation|state transition|concurrency|idempotency|masking|expiry|version binding)\b|\b\d+\s*(days?|hours?|minutes?|characters?|items?)\b'
    if ($interactionText -match $policyLeakPattern) {
      Add-Error "$($file.Name): trigger, condition, or flow content may disclose policy or cite a Business Rule."
    }
    $relatedApis = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($match in [regex]::Matches($text, 'API-[A-Z0-9-]+')) {
      [void]$apiReferences.Add($match.Value)
      [void]$relatedApis.Add($match.Value)
    }
    if ($ucHeading.Success) { $ucRelatedApis["UC-$ucNumber"] = $relatedApis }
  } else {
    $heading = [regex]::Match($text, '(?m)^# (API-[A-Z0-9-]+) — ')
    if ($heading.Success) {
      $apiId = $heading.Groups[1].Value
      [void]$apiDefinitions.Add($apiId)

      if ($text -match '(?m)^\s*\|') {
        Add-Error "$($file.Name): API contracts must use a sequential layout without Markdown tables."
      }
      if ($text -match '(?im)```(?:plantuml|ocl)|\bBR-API-[A-Z0-9-]+\b|^##+ UML Model\s*$|^##+ Business Rules') {
        Add-Error "$($file.Name): API contracts must not contain UML, OCL, or API rule definitions."
      }

      $levelTwoHeadings = @([regex]::Matches($text, '(?m)^## (.+)\r?$') |
        ForEach-Object { $_.Groups[1].Value.Trim() })
      $requiredPrefix = @(
        'API ID',
        'API Name',
        'Related Use Case IDs',
        'Method',
        'Path',
        'Description',
        'Authentication',
        'Authorization',
        'Request Headers',
        'Path Parameters',
        'Query Parameters',
        'Request Body'
      )
      if ($levelTwoHeadings.Count -lt 15) {
        Add-Error "$($file.Name): incomplete sequential API section set."
      } else {
        for ($headingIndex = 0; $headingIndex -lt $requiredPrefix.Count; $headingIndex++) {
          if ($levelTwoHeadings[$headingIndex] -ne $requiredPrefix[$headingIndex]) {
            Add-Error "$($file.Name): expected '## $($requiredPrefix[$headingIndex])' at sequential position $($headingIndex + 1)."
            break
          }
        }
        $tailHeadings = @($levelTwoHeadings[$requiredPrefix.Count..($levelTwoHeadings.Count - 1)])
        $successHeadings = @($tailHeadings | Where-Object { $_ -match '^Success Response — HTTP \d{3}$' })
        $errorHeadings = @($tailHeadings | Where-Object { $_ -match '^Error Response — HTTP \d{3}$' })
        if ($successHeadings.Count -eq 0) {
          Add-Error "$($file.Name): at least one success-response section is required."
        }
        if ($errorHeadings.Count -eq 0) {
          Add-Error "$($file.Name): at least one error-response section is required."
        }
        if ($levelTwoHeadings[-1] -ne 'Notes') {
          Add-Error "$($file.Name): Notes must be the final level-two section."
        }
        $unexpectedTail = @($tailHeadings | Where-Object {
          $_ -ne 'Notes' -and
          $_ -notmatch '^Success Response — HTTP \d{3}$' -and
          $_ -notmatch '^Error Response — HTTP \d{3}$'
        })
        if ($unexpectedTail.Count -gt 0) {
          Add-Error "$($file.Name): unexpected sequential API section: $($unexpectedTail[0])"
        }
      }

      $declaredApiId = [regex]::Match($text, '(?ms)^## API ID\s*\r?\n\s*`(API-[A-Z0-9-]+)`')
      if (-not $declaredApiId.Success -or $declaredApiId.Groups[1].Value -ne $apiId) {
        Add-Error "$($file.Name): API ID value must match the top-level heading."
      }

      $relatedSection = [regex]::Match(
        $text,
        '(?ms)^## Related Use Case IDs\s*\r?\n(.*?)(?=^## |\z)'
      )
      $relatedUcs = [System.Collections.Generic.List[string]]::new()
      if ($relatedSection.Success) {
        foreach ($ucMatch in [regex]::Matches($relatedSection.Groups[1].Value, '`(UC-\d{2})`')) {
          if (-not $relatedUcs.Contains($ucMatch.Groups[1].Value)) {
            $relatedUcs.Add($ucMatch.Groups[1].Value)
          }
        }
      }
      if ($relatedUcs.Count -eq 0) {
        Add-Error "$($file.Name): Related Use Case IDs must contain at least one UC ID."
      }
      $apiRelatedUcs[$apiId] = $relatedUcs

      foreach ($fieldMatch in [regex]::Matches(
        $text,
        '(?ms)^### `[^`]+`\s*\r?\n(.*?)(?=^### |^## |\z)'
      )) {
        $fieldBody = $fieldMatch.Groups[1].Value
        foreach ($metadata in @('Type', 'Required', 'Nullable')) {
          if ($fieldBody -notmatch "(?m)^- ${metadata}: .+") {
            Add-Error "$($file.Name): every field definition needs $metadata metadata."
          }
        }
      }

      $apiPolicyLeakPattern = '(?i)(>=|<=|(?<!-)\bgreater than\b|\bless than\b|\bat least\b|\bat most\b|\bminimum\b|\bmaximum\b|\bmust differ\b|\bnot earlier\b|\bnot later\b|\bexists?\b|\bunique\b|\bactive\b|\binactive\b|\beligib|\bowner|\bavailable if\b|\bexpired\b|\bprice changed\b|\bavailability changed\b|\bcapacity\b|\branking formula\b|\bstate transition\b|\bmatches another field\b)'
      foreach ($line in ($text -split '\r?\n')) {
        if ($line -match '^- (Validation|Trigger):' -and $line -match $apiPolicyLeakPattern) {
          Add-Error "$($file.Name): API validation or trigger may disclose domain policy: $line"
        }
      }
    }
  }

  if ($text -match '[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ]') {
    Add-Error "$($file.Name): non-English Vietnamese characters detected."
  }

  foreach ($linkMatch in [regex]::Matches($text, '\[[^\]]+\]\(([^)]+)\)')) {
    $link = $linkMatch.Groups[1].Value
    if ($link -notmatch '^(https?://|#)') {
      $target = [System.IO.Path]::GetFullPath((Join-Path $file.DirectoryName $link))
      if (-not (Test-Path -LiteralPath $target)) {
        Add-Error "$($file.Name): missing relative link $link"
      }
    }
  }
}

foreach ($reference in $apiReferences) {
  if (-not $apiDefinitions.Contains($reference)) {
    Add-Error "UC references undefined API: $reference"
  }
}

foreach ($ucId in $ucRelatedApis.Keys) {
  foreach ($apiId in $ucRelatedApis[$ucId]) {
    if ($apiDefinitions.Contains($apiId) -and
        (-not $apiRelatedUcs.ContainsKey($apiId) -or -not $apiRelatedUcs[$apiId].Contains($ucId))) {
      Add-Error "$ucId lists $apiId, but $apiId does not reference $ucId."
    }
  }
}

foreach ($apiId in $apiRelatedUcs.Keys) {
  foreach ($ucId in $apiRelatedUcs[$apiId]) {
    if (-not $ucDefinitions.Contains($ucId)) {
      Add-Error "$apiId references undefined use case: $ucId"
      continue
    }
    $ucFile = @($ucFiles | Where-Object {
      (Get-Content -Encoding UTF8 -Raw -LiteralPath $_.FullName) -match "(?m)^# $ucId — "
    }) | Select-Object -First 1
    if ($null -ne $ucFile) {
      $ucText = Get-Content -Encoding UTF8 -Raw -LiteralPath $ucFile.FullName
      if ($ucText -notmatch "\b$([regex]::Escape($apiId))\b") {
        Add-Error "$apiId lists $ucId, but $ucId does not reference $apiId."
      }
    }
  }
}

if (-not $SkipDbmlCompile -and (Test-Path -LiteralPath (Join-Path $rootPath 'schema.dbml'))) {
  $tempSql = Join-Path ([System.IO.Path]::GetTempPath()) ("figma-spec-" + [guid]::NewGuid().ToString('N') + '.sql')
  $compileWorkingDirectory = Split-Path -Parent $tempSql
  try {
    Push-Location -LiteralPath $compileWorkingDirectory
    try {
      $dbmlCommand = Get-Command dbml2sql -ErrorAction SilentlyContinue
      if ($dbmlCommand) {
        & $dbmlCommand.Source (Join-Path $rootPath 'schema.dbml') --postgres -o $tempSql | Out-Null
      } elseif (Get-Command npx -ErrorAction SilentlyContinue) {
        npx --yes --package @dbml/cli dbml2sql (Join-Path $rootPath 'schema.dbml') --postgres -o $tempSql | Out-Null
      } else {
        Add-Error 'DBML compiler unavailable; install @dbml/cli or use -SkipDbmlCompile.'
      }
    } finally {
      Pop-Location
    }
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $tempSql)) {
      Add-Error 'schema.dbml did not compile to PostgreSQL SQL.'
    }
  } finally {
    if (Test-Path -LiteralPath $tempSql) { Remove-Item -LiteralPath $tempSql -Force }
  }
}

if ($errors.Count -gt 0) {
  $errors | ForEach-Object { [Console]::Error.WriteLine($_) }
  exit 1
}

Write-Output "PASS: $($ucFiles.Count) UC files, $($apiFiles.Count) sequential API files, $($allBehaviorIds.Count) coded conditions and branch flows, $allFlowActivityCount numbered flow activities, $($allRuleIds.Count) unique UC OCL rules."
