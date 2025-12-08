{{- /* Trivy HTML Template */ -}}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trivy Security Scan Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }
        
        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .summary-card .number {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .summary-card .label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .critical-card { border-top: 4px solid #d32f2f; }
        .critical-card .number { color: #d32f2f; }
        
        .high-card { border-top: 4px solid #f57c00; }
        .high-card .number { color: #f57c00; }
        
        .medium-card { border-top: 4px solid #fbc02d; }
        .medium-card .number { color: #fbc02d; }
        
        .low-card { border-top: 4px solid #689f38; }
        .low-card .number { color: #689f38; }
        
        .info-section {
            padding: 30px;
            background: white;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-section h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .info-item {
            padding: 12px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }
        
        .info-item strong {
            color: #667eea;
            display: inline-block;
            min-width: 120px;
        }
        
        .vulnerabilities-section {
            padding: 30px;
        }
        
        .vulnerabilities-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .target-section {
            margin-bottom: 40px;
        }
        
        .target-header {
            background: #667eea;
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .vuln-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 0 0 8px 8px;
            overflow: hidden;
        }
        
        .vuln-table thead {
            background: #f8f9fa;
        }
        
        .vuln-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #e0e0e0;
            position: sticky;
            top: 0;
            background: #f8f9fa;
            z-index: 10;
        }
        
        .vuln-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: top;
        }
        
        .vuln-table tbody tr {
            background: white;
            transition: background-color 0.2s;
        }
        
        .vuln-table tbody tr:hover {
            background: #f8f9fa;
        }
        
        .severity-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .severity-CRITICAL {
            background: #d32f2f;
            color: white;
        }
        
        .severity-HIGH {
            background: #f57c00;
            color: white;
        }
        
        .severity-MEDIUM {
            background: #fbc02d;
            color: #333;
        }
        
        .severity-LOW {
            background: #689f38;
            color: white;
        }
        
        .severity-UNKNOWN {
            background: #757575;
            color: white;
        }
        
        .vuln-id {
            color: #667eea;
            font-weight: 600;
            text-decoration: none;
        }
        
        .vuln-id:hover {
            text-decoration: underline;
        }
        
        .package-name {
            font-family: 'Courier New', monospace;
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        
        .version {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .no-vulnerabilities {
            text-align: center;
            padding: 40px;
            color: #689f38;
            font-size: 1.2em;
        }
        
        .no-vulnerabilities::before {
            content: "✓";
            display: block;
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        .description {
            font-size: 0.9em;
            color: #555;
            line-height: 1.5;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
            }
            
            .summary-card:hover,
            .vuln-table tbody tr:hover {
                transform: none;
                background: white;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Trivy Security Scan Report</h1>
            <div class="subtitle">Comprehensive Vulnerability Analysis</div>
        </div>
        
        {{- /* Calculate summary statistics */ -}}
        {{- $criticalCount := 0 -}}
        {{- $highCount := 0 -}}
        {{- $mediumCount := 0 -}}
        {{- $lowCount := 0 -}}
        {{- range . -}}
            {{- range .Vulnerabilities -}}
                {{- if eq .Severity "CRITICAL" -}}
                    {{- $criticalCount = add $criticalCount 1 -}}
                {{- else if eq .Severity "HIGH" -}}
                    {{- $highCount = add $highCount 1 -}}
                {{- else if eq .Severity "MEDIUM" -}}
                    {{- $mediumCount = add $mediumCount 1 -}}
                {{- else if eq .Severity "LOW" -}}
                    {{- $lowCount = add $lowCount 1 -}}
                {{- end -}}
            {{- end -}}
        {{- end -}}
        
        <div class="summary">
            <div class="summary-card critical-card">
                <div class="label">Critical</div>
                <div class="number">{{ $criticalCount }}</div>
            </div>
            <div class="summary-card high-card">
                <div class="label">High</div>
                <div class="number">{{ $highCount }}</div>
            </div>
            <div class="summary-card medium-card">
                <div class="label">Medium</div>
                <div class="number">{{ $mediumCount }}</div>
            </div>
            <div class="summary-card low-card">
                <div class="label">Low</div>
                <div class="number">{{ $lowCount }}</div>
            </div>
        </div>
        
        {{- if . -}}
        <div class="info-section">
            <h2>Scan Information</h2>
            <div class="info-grid">
                {{- with (index . 0) -}}
                <div class="info-item">
                    <strong>Target:</strong> {{ .Target }}
                </div>
                <div class="info-item">
                    <strong>Type:</strong> {{ .Type }}
                </div>
                {{- end -}}
                <div class="info-item">
                    <strong>Total Vulnerabilities:</strong> {{ add $criticalCount $highCount $mediumCount $lowCount }}
                </div>
                <div class="info-item">
                    <strong>Scan Date:</strong> <span id="scan-date"></span>
                </div>
            </div>
        </div>
        {{- end -}}
        
        <div class="vulnerabilities-section">
            <h2>Detected Vulnerabilities</h2>
            
            {{- $hasVulnerabilities := false -}}
            {{- range . -}}
                {{- if .Vulnerabilities -}}
                    {{- $hasVulnerabilities = true -}}
                {{- end -}}
            {{- end -}}
            
            {{- if not $hasVulnerabilities -}}
            <div class="no-vulnerabilities">
                No vulnerabilities detected! Your image is secure.
            </div>
            {{- else -}}
            
            {{- range . -}}
                {{- if .Vulnerabilities -}}
                <div class="target-section">
                    <div class="target-header">
                        {{ .Target }} ({{ .Type }})
                    </div>
                    <table class="vuln-table">
                        <thead>
                            <tr>
                                <th style="width: 12%;">Severity</th>
                                <th style="width: 15%;">Vulnerability ID</th>
                                <th style="width: 18%;">Package</th>
                                <th style="width: 10%;">Installed</th>
                                <th style="width: 10%;">Fixed In</th>
                                <th style="width: 35%;">Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {{- range .Vulnerabilities -}}
                            <tr>
                                <td>
                                    <span class="severity-badge severity-{{ .Severity }}">
                                        {{ .Severity }}
                                    </span>
                                </td>
                                <td>
                                    {{- if .PrimaryURL -}}
                                    <a href="{{ .PrimaryURL }}" class="vuln-id" target="_blank">
                                        {{ .VulnerabilityID }}
                                    </a>
                                    {{- else -}}
                                    <span class="vuln-id">{{ .VulnerabilityID }}</span>
                                    {{- end -}}
                                </td>
                                <td>
                                    <span class="package-name">{{ .PkgName }}</span>
                                </td>
                                <td>
                                    <span class="version">{{ .InstalledVersion }}</span>
                                </td>
                                <td>
                                    {{- if .FixedVersion -}}
                                    <span class="version">{{ .FixedVersion }}</span>
                                    {{- else -}}
                                    <span style="color: #999;">N/A</span>
                                    {{- end -}}
                                </td>
                                <td>
                                    <div class="description">
                                        {{- if .Title -}}
                                            {{ .Title }}
                                        {{- else if .Description -}}
                                            {{ .Description }}
                                        {{- else -}}
                                            No description available
                                        {{- end -}}
                                    </div>
                                </td>
                            </tr>
                            {{- end -}}
                        </tbody>
                    </table>
                </div>
                {{- end -}}
            {{- end -}}
            {{- end -}}
        </div>
        
        <div class="footer">
            Generated by Trivy Security Scanner | 
            <span id="generation-time"></span>
        </div>
    </div>
    
    <script>
        // Set current date/time
        const now = new Date();
        document.getElementById('scan-date').textContent = now.toLocaleString();
        document.getElementById('generation-time').textContent = now.toLocaleString();
    </script>
</body>
</html>
