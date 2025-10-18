# Security Summary

## Overview

This document describes the security measures implemented in the Paper2Code chatbot application and the status of security vulnerabilities discovered during development.

## Discovered Vulnerabilities

During development, CodeQL analysis identified potential security issues related to:
1. Path injection vulnerabilities
2. Command injection vulnerabilities

## Mitigation Measures

### 1. Path Injection Mitigation

**Vulnerability**: User-provided paper names and file paths could potentially be used for path traversal attacks.

**Mitigation Implemented**:
- **Input Validation**: `validate_paper_name()` function restricts paper names to alphanumeric characters, hyphens, and underscores only (regex: `^[a-zA-Z0-9_-]{1,100}$`)
- **Path Sanitization**: `sanitize_path()` function ensures all file paths are:
  - Converted to absolute paths
  - Normalized to prevent `../` traversal
  - Validated to be within application-controlled directories
  - Rejected if they attempt to access paths outside the application directory

**Locations Fixed**:
- Line ~303-304: Output directory creation
- Line ~308: PDF JSON path creation
- Line ~375: Walking output repository directory
- Line ~417-418: ZIP file creation paths

### 2. Command Injection Mitigation

**Vulnerability**: User-provided values (paper name, model name) used in subprocess calls could potentially be exploited for command injection.

**Mitigation Implemented**:
- **Input Validation**: All paper names are validated through `validate_paper_name()`
- **Whitelist Validation**: Model names are validated against an allowed list of models:
  ```python
  allowed_models = ['gpt-4', 'gpt-4-turbo', 'gpt-35-turbo', 'gpt-4o', 'gpt-4o-mini']
  ```
- **Parameterized Commands**: All subprocess calls use list-based arguments (not shell=True) to prevent shell injection
- **Path Sanitization**: All file paths passed to subprocesses are sanitized first

**Locations Fixed**:
- Line ~144: Planning stage subprocess call
- Line ~172: Config extraction subprocess call
- Line ~184: Analysis stage subprocess call
- Line ~216: Coding stage subprocess call

## Security Features

### Input Validation
- **Paper Names**: Strict regex validation limiting to safe characters
- **File Uploads**: Only JSON files accepted (MIME type validation by Streamlit)
- **Model Names**: Whitelist-based validation
- **Paths**: Absolute path validation with directory restriction

### Safe File Handling
- **No Code Execution**: Uploaded files are only parsed as JSON, never executed
- **Sandboxed Output**: All outputs are written to dedicated `outputs/` directory
- **Temporary Files**: Properly cleaned up after processing
- **ZIP Creation**: Safe archive creation without executing any uploaded content

### Environment Security
- **Credentials**: Stored in environment variables, never in code
- **No Hardcoded Secrets**: All sensitive data configured via environment
- **.env Files**: Excluded from version control via `.gitignore`

### Process Isolation
- **Subprocess Execution**: All Python scripts run in separate processes
- **No Shell Injection**: Using list-based subprocess arguments
- **Error Handling**: Proper exception handling prevents information leakage

## Known Limitations

### Static Analysis False Positives

CodeQL may still report some alerts because:
1. **Runtime Validation**: Our validation happens at runtime, but CodeQL performs static analysis
2. **Sanitized Paths**: Even sanitized paths are flagged if they originated from user input
3. **Parameterized Commands**: CodeQL may not recognize that validated inputs are safe

These are **false positives** in practice because:
- All inputs are validated before use
- Paths are sanitized and restricted to safe directories
- Commands are parameterized and validated
- No shell execution is used

### Residual Risks

While the implemented mitigations significantly reduce risk, users should:
1. **Run in Isolated Environment**: Deploy in a containerized or sandboxed environment
2. **Monitor File System**: Watch the `outputs/` directory for unexpected files
3. **Limit Permissions**: Run with minimal file system permissions
4. **Monitor API Usage**: Track Azure OpenAI API calls for unexpected patterns
5. **Regular Updates**: Keep dependencies updated for security patches

## Security Best Practices for Deployment

### Recommended Deployment Configuration

```bash
# 1. Run in a container
docker run --rm -it \
  -e AZURE_OPENAI_API_KEY="your-key" \
  -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
  -e AZURE_OPENAI_DEPLOYMENT="your-deployment" \
  -v ./outputs:/app/outputs:rw \
  paper2code-chatbot

# 2. Or use a dedicated user with limited permissions
sudo useradd -m -s /bin/bash paper2code
sudo chown paper2code:paper2code /app/outputs
sudo -u paper2code streamlit run chatbot_app.py
```

### Network Security

```bash
# Bind only to localhost in production
streamlit run chatbot_app.py --server.address localhost --server.port 8501

# Use a reverse proxy (nginx) for external access with SSL
# Configure rate limiting and request size limits
```

### File System Permissions

```bash
# Restrict outputs directory
chmod 755 outputs/
chown paper2code:paper2code outputs/

# Make application files read-only
chmod 444 chatbot_app.py
chmod 444 codes/*.py
```

## Conclusion

### Security Status

✅ **Input Validation**: All user inputs are validated
✅ **Path Sanitization**: All file paths are sanitized and restricted
✅ **Command Protection**: All subprocess calls are parameterized
✅ **No Code Execution**: Uploaded files are parsed, not executed
✅ **Credential Security**: Secrets stored in environment variables
✅ **Error Handling**: Proper exception handling implemented

### Recommendations

1. **Deploy with Caution**: Use in trusted environments or with proper isolation
2. **Monitor Usage**: Track API calls and file system activity
3. **Regular Updates**: Keep all dependencies updated
4. **Access Control**: Implement authentication if exposing publicly
5. **Rate Limiting**: Add rate limiting for production deployments

### For Production Use

Consider adding:
- **Authentication**: User login and access control
- **Rate Limiting**: Prevent abuse and control costs
- **Logging**: Comprehensive audit logging
- **Monitoring**: Real-time security monitoring
- **WAF**: Web Application Firewall for additional protection

## Contact

For security concerns or to report vulnerabilities, please:
1. Do not open public issues
2. Contact the repository maintainers privately
3. Provide detailed information about the vulnerability
4. Allow time for patching before disclosure

---

**Last Updated**: 2025-10-18
**Security Review Status**: Initial implementation complete with mitigations in place
