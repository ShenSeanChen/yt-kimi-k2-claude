# Claude Code + Kimi K2 Integration Setup Guide
**Directory**: `/Users/your_computer/your_local_path/`

This guide explains every step needed to set up Claude Code with Kimi K2 integration, including why each step is necessary.

## 🎯 **Overview: What We're Building**

We're setting up Claude Code (Anthropic's CLI tool) to work with **Kimi K2** (Moonshot AI's 1T parameter model) instead of the default Claude models. This gives us access to Kimi K2's superior coding and agentic capabilities through a familiar interface.

---

## 📋 **Step-by-Step Setup**

### **Step 1: Install Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
```

**Why this step is needed:**
- Claude Code is Anthropic's official CLI tool for AI-assisted coding
- The `-g` flag installs it globally, making the `claude` command available system-wide
- This gives us a professional, feature-rich interface for interacting with AI models

### **Step 2: Fix PATH Configuration**
```bash
# Check where npm installed Claude Code
npm list -g @anthropic-ai/claude-code

# Add npm global bin to PATH (temporary fix)
export PATH="/Users/your_computer/.npm-global/bin:$PATH"

# Permanent fix - add to shell profile
echo 'export PATH="/Users/your_computer/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify it works
claude --version
```

**Why this step is needed:**
- npm installed Claude Code to a custom directory (`~/.npm-global/bin`)
- This directory wasn't in your system's PATH environment variable
- Without PATH configuration, the shell can't find the `claude` command
- The permanent fix ensures the command works in all future terminal sessions

### **Step 3: Bypass Region Restrictions**
```bash
# Create a proper Node.js script to fix the configuration
cat > fix_claude_config.js << 'EOF'
const os = require('os');
const fs = require('fs');
const path = require('path');

const homeDir = os.homedir();
const filePath = path.join(homeDir, '.claude.json');

if (fs.existsSync(filePath)) {
    const content = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    fs.writeFileSync(filePath, JSON.stringify({ ...content, hasCompletedOnboarding: true }, null, 2), 'utf-8');
    console.log('Updated existing .claude.json');
} else {
    fs.writeFileSync(filePath, JSON.stringify({ hasCompletedOnboarding: true }, null, 2), 'utf-8');
    console.log('Created new .claude.json');
}
EOF

# Run the script
node fix_claude_config.js

# Clean up
rm fix_claude_config.js
```

**Why this step is needed:**
- Claude Code normally performs region/country verification
- This verification can block access in certain regions
- Setting `hasCompletedOnboarding: true` bypasses this check
- The original command in the PDF had line break issues causing syntax errors
- Our fixed version properly handles the JSON configuration

### **Step 4: Configure Kimi K2 API Access**
```bash
# Set up environment variables for Kimi K2 access
export ANTHROPIC_AUTH_TOKEN="sk-your-moonshot-api-key"
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"

# Make it permanent
echo 'export ANTHROPIC_AUTH_TOKEN="sk-your-moonshot-api-key"' >> ~/.zshrc
echo 'export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"' >> ~/.zshrc
source ~/.zshrc
```

**Why this step is needed:**
- Claude Code was designed for Anthropic's API, but we want to use Kimi K2
- `ANTHROPIC_AUTH_TOKEN`: Your Moonshot AI API key (starts with `sk-`)
- `ANTHROPIC_BASE_URL`: Redirects API calls to Moonshot's servers instead of Anthropic's
- This allows Claude Code's interface to work with Kimi K2's backend

### **Step 5: Test the Setup**
```bash
# Navigate to your project directory
cd /Users/your_computer/your_local_path

# Launch Claude Code
claude
```

**Why this step is needed:**
- Verifies that all configuration steps worked correctly
- You should see Claude Code's interface without region verification prompts
- The tool will now use Kimi K2 for AI assistance instead of Claude models

---

## 🔧 **Technical Architecture**

```
Your Terminal
      ↓
Claude Code CLI (Anthropic's interface)
      ↓
ANTHROPIC_BASE_URL redirect
      ↓
Moonshot AI API (api.moonshot.cn)
      ↓
Kimi K2 Model (1T parameters, MoE architecture)
```

This guide explains:

1. **Why we install Claude Code**: Professional CLI interface with rich features
2. **Why we fix PATH**: System integration so commands work globally  
3. **Why we bypass region checks**: Global access without geographic restrictions
4. **Why we redirect APIs**: Access Kimi K2's superior performance through familiar interface
5. **Why each environment variable matters**: Proper authentication and routing

The key insight is that we're using Claude Code as a **high-quality interface** while **redirecting the backend** to Kimi K2's more powerful model. This gives us the best of both worlds: proven UX + cutting-edge AI capabilities!

---

## 🚀 **Why Each Component Matters**

### **Claude Code CLI**
- **Professional Interface**: Syntax highlighting, file context, git integration
- **Proven Workflow**: Battle-tested by thousands of developers
- **Rich Features**: Project awareness, multi-file editing, conversation history

### **PATH Configuration**
- **System Integration**: Makes commands available globally
- **Shell Compatibility**: Works across different terminal sessions
- **Developer Experience**: No need to remember full paths

### **Region Bypass**
- **Global Access**: Works regardless of geographic location
- **Simplified Setup**: Skips unnecessary verification steps
- **Faster Onboarding**: Direct access to the tool

### **API Redirection**
- **Model Flexibility**: Use any compatible API backend
- **Cost Optimization**: Access to potentially cheaper/better models
- **Performance**: Kimi K2's superior benchmarks vs. standard Claude

---

## 📊 **Kimi K2 vs Claude Comparison**

| Benchmark | Kimi K2 | Claude Sonnet 4 | Advantage |
|-----------|---------|-----------------|-----------|
| LiveCodeBench v6 | 53.7% | 47.4% | **+6.3%** |
| AIME 2024 | 69.6% | 43.4% | **+26.2%** |
| Tool Use (Berkeley) | 90.2% | ~85% | **+5.2%** |
| Agentic Benchmarks | 70.6% | ~65% | **+5.6%** |

---

## 🎉 **Next Steps**

1. **Test Basic Functionality**: Ask Kimi K2 to help with a simple coding task
2. **Explore Agentic Features**: Try multi-step workflows and tool calling
3. **Benchmark Performance**: Compare with your previous Claude experience
4. **Build Projects**: Use Kimi K2's superior coding abilities for real work

---

## 🐛 **Troubleshooting**

### Command Not Found
```bash
# Check installation
npm list -g @anthropic-ai/claude-code

# Fix PATH
export PATH="/Users/your_computer/.npm-global/bin:$PATH"
```

### API Authentication Issues
```bash
# Verify environment variables
echo $ANTHROPIC_AUTH_TOKEN
echo $ANTHROPIC_BASE_URL

# Re-export if needed
export ANTHROPIC_AUTH_TOKEN="sk-your-key"
export ANTHROPIC_BASE_URL="https://api.moonshot.cn/anthropic"
```

### Region Verification Prompts
```bash
# Check config file
cat ~/.claude.json

# Should contain: {"hasCompletedOnboarding": true}
```

---

**🎯 You're now ready to experience Kimi K2's state-of-the-art AI capabilities through Claude Code's professional interface!**
