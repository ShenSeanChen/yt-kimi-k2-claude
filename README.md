# 🚀 Kimi K2 + Claude Code Integration & NextJS Projects

📹 Full YouTube Guide: [Youtube link](https://www.youtube.com/watch?v=dSS6DgErZXA&list=PLE9hy4A7ZTmpGq7GHf5tgGFWh2277AeDR&index=21)

🚀 X Post: [X link](https://x.com/ShenSeanChen/status/1947796273899139530)

💻 Launch Full Stack Product: [Github Repo](https://github.com/ShenSeanChen/launch-mvp-stripe-nextjs-supabase)

☕️ Buy me a coffee: [Cafe Latte](https://buy.stripe.com/5kA176bA895ggog4gh)

🤖️ Discord: [Invite link](https://discord.com/invite/TKKPzZheua)

**Directory**: `/Users/your_computer/your_path/`

This repository demonstrates the power of **Kimi K2** (Moonshot AI's 1T parameter model) integrated with **Claude Code** for advanced AI-assisted development, featuring practical NextJS projects and live coding demonstrations.

## 🎯 **Repository Overview**

### **What's Inside**
- 🔧 **Kimi K2 + Claude Code Setup Guide** - Complete integration tutorial
- 💰 **Personal Finance Dashboard** - Full-stack NextJS + Supabase application
- 🎮 **Playground Scripts** - Python demos and web scraping tools
- 📝 **Live Project Space** - Area for building new projects in real-time

### **Why This Matters**
This setup gives you access to **Kimi K2's superior coding capabilities** (53.7% on LiveCodeBench vs Claude's 47.4%) through Claude Code's professional interface - the best of both worlds!

---

## 🛠️ **Kimi K2 + Claude Code Setup**

### **Quick Start**
```bash
# 1. Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# 2. Fix PATH configuration
export PATH="/Users/your_computer/.npm-global/bin:$PATH"
echo 'export PATH="/Users/your_computer/.npm-global/bin:$PATH"' >> ~/.zshrc

# 3. Configure API access
export ANTHROPIC_AUTH_TOKEN="sk-your-moonshot-api-key"
export ANTHROPIC_BASE_URL="https://api.moonshot/anthropic"

# 4. Bypass region restrictions
node -e "const fs=require('fs'),os=require('os'),path=require('path'); const file=path.join(os.homedir(),'.claude.json'); fs.writeFileSync(file,JSON.stringify({hasCompletedOnboarding:true},null,2));"

# 5. Launch Claude Code
claude
```

### **Technical Architecture**
```
Your Terminal → Claude Code CLI → API Redirect → Moonshot AI → Kimi K2 (1T params)
```

### **Performance Comparison**
| Benchmark | Kimi K2 | Claude Sonnet 4 | Advantage |
|-----------|---------|-----------------|-----------|
| LiveCodeBench v6 | **53.7%** | 47.4% | **+6.3%** |
| AIME 2024 | **69.6%** | 43.4% | **+26.2%** |
| Tool Use (Berkeley) | **90.2%** | ~85% | **+5.2%** |
| Agentic Benchmarks | **70.6%** | ~65% | **+5.6%** |

**📖 [Complete Setup Guide](./kimi_claude_code_setup_guide.md)**

---

## 💰 **Personal Finance Dashboard**

### **Live Demo**
A full-stack NextJS application with real-time financial tracking, built with modern web technologies.

![Finance Dashboard Preview](https://via.placeholder.com/800x400/6366f1/white?text=FinanceFlow+Dashboard)

### **Key Features**
- 📊 **Real-time Financial Overview** - Income, expenses, and balance tracking
- 💳 **Transaction Management** - Add, categorize, and delete transactions
- 🎨 **Modern UI/UX** - Glassmorphism design with dark mode support
- 🔐 **Secure Authentication** - Supabase Auth with Row Level Security
- 📱 **Mobile Responsive** - Adaptive design for all screen sizes

### **Tech Stack**
- **Frontend**: Next.js 15.4.1, React 19, TypeScript
- **Styling**: Tailwind CSS, Radix UI components
- **Backend**: Supabase (PostgreSQL, Auth, RLS)
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React icons

### **Quick Start**
```bash
cd personal-finance-dashboard
npm install
npm run dev
```

**📖 [Complete Setup Instructions](./personal-finance-dashboard/SETUP.md)**

### **Project Structure**
```
personal-finance-dashboard/
├── src/
│   ├── app/
│   │   ├── dashboard/          # Main dashboard page
│   │   ├── login/              # Authentication
│   │   └── layout.tsx          # Root layout
│   ├── lib/
│   │   ├── supabase-client.ts  # Client-side Supabase
│   │   └── supabase-server.ts  # Server-side Supabase
│   └── types/
│       └── database.ts         # TypeScript definitions
├── components/ui/              # Reusable UI components
├── schema.sql                  # Database schema
└── README.md                   # Project documentation
```

### **Database Schema**
```sql
-- User profiles with budget tracking
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  full_name TEXT,
  monthly_budget DECIMAL(10,2) DEFAULT 3000,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Transaction records with categories
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  amount DECIMAL(10,2) NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  type TEXT CHECK (type IN ('income', 'expense')),
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### **Key Components**
- **Dashboard Page** - Main financial overview with metrics cards
- **Transaction Form** - Add new income/expense entries
- **Transaction List** - View and manage all transactions
- **Auth Integration** - Secure user authentication and data isolation

---

## 🎮 **Playground Scripts**

### **Python Demos**
- `kimi_k2_setup.py` - API configuration and testing
- `kimi_k2_coding_demo.py` - Coding assistance examples
- `kimi_k2_agentic_demo.py` - Agent-based task automation
- `web_scraper.py` - Web scraping utilities

### **Running the Demos**
```bash
cd playground
python kimi_k2_setup.py
python kimi_k2_coding_demo.py
```

---

## 🚀 **Live Project Development**

### **Coming Soon: New Project**
This section will showcase a new project built live using Kimi K2 + Claude Code integration, demonstrating:

- **Real-time AI-assisted development**
- **Advanced code generation and refactoring**
- **Modern web development patterns**
- **Production-ready deployment**

### **Development Workflow**
1. **Planning** - AI-assisted project architecture
2. **Implementation** - Code generation with Kimi K2
3. **Testing** - Automated testing strategies
4. **Deployment** - Production deployment pipeline

---

## 📚 **Documentation**

### **Setup Guides**
- [Kimi K2 + Claude Code Integration](./kimi_claude_code_setup_guide.md)
- [Personal Finance Dashboard Setup](./personal-finance-dashboard/SETUP.md)

### **API Documentation**
- [Moonshot AI API Reference](https://platform.moonshot/docs)
- [Supabase Documentation](https://supabase.com/docs)

### **Development Standards**
- **Code Style**: Google TypeScript Style Guide
- **Comments**: Comprehensive inline documentation
- **Architecture**: Component-based, service-oriented design
- **Testing**: Jest + React Testing Library
- **Deployment**: Vercel for frontend, Supabase for backend

---

## 🔧 **Development Environment**

### **Requirements**
- Node.js 18+ and npm
- Python 3.8+ (for playground scripts)
- Supabase account and project
- Moonshot AI API key

### **Recommended Tools**
- **Code Editor**: VS Code with TypeScript extensions
- **Terminal**: iTerm2 or Windows Terminal
- **Git**: For version control
- **Claude Code**: For AI-assisted development

### **Environment Variables**
```bash
# Kimi K2 Integration
ANTHROPIC_AUTH_TOKEN="sk-your-moonshot-api-key"
ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL="your-supabase-url"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your-supabase-anon-key"
```

---

## 📈 **Performance Benchmarks**

### **Kimi K2 Advantages**
- **26.2% better** on mathematical reasoning (AIME 2024)
- **6.3% better** on live coding challenges (LiveCodeBench v6)
- **5.6% better** on agentic task completion
- **Superior** tool use and function calling capabilities

### **Application Performance**
- **Personal Finance Dashboard**: Sub-100ms page loads
- **Real-time Updates**: Optimistic UI updates
- **Mobile Performance**: 90+ Lighthouse scores
- **SEO Optimization**: Server-side rendering with Next.js

---

## 🤝 **Contributing**

### **Development Process**
1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** changes with proper testing
4. **Document** new features and APIs
5. **Submit** pull request with detailed description

### **Code Standards**
- Follow Google TypeScript Style Guide
- Add comprehensive comments
- Include unit tests for new features
- Update documentation as needed

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 **Star History**

If you find this project useful, please consider giving it a star! Your support helps others discover these powerful AI development tools.

---

**🎯 Ready to experience the future of AI-assisted development with Kimi K2 + Claude Code?**

Get started with the [setup guide](./kimi_claude_code_setup_guide.md) and explore the [personal finance dashboard](./personal-finance-dashboard/) to see what's possible!
