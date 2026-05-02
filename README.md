# 🚀 LangGraph Stock Chatbot with Human-in-the-Loop (HITL)

An advanced **Agentic AI chatbot** built using **LangGraph + Groq**, supporting:

* 💬 Normal conversational chatbot
* 📈 Real-time stock price lookup
* 💰 Buy/Sell stock simulation
* 👤 Human-in-the-Loop (HITL) approval system
* 📊 Portfolio tracking

---

## 📌 Features

### 🤖 Chatbot

* Works like a normal AI assistant
* Answers general questions naturally

---

### 📈 Stock Tools

* Get stock price (e.g., AAPL, TSLA)
* Buy stocks (with human approval)
* Sell stocks (with validation + approval)
* View portfolio

---

### 👤 Human-in-the-Loop (HITL)

* Approval required before:

  * Buying stock
  * Selling stock

Popup UI:

* ✅ Yes → Execute action
* ❌ No → Cancel action

---

### 📊 Portfolio Management

* Tracks owned stocks
* Prevents invalid operations:

  * Selling more than owned ❌
  * Selling without owning ❌

---

## 🏗️ Architecture

```plaintext
User → Streamlit UI
      ↓
LangGraph (chat_node)
      ↓
Groq LLM (llama3)
      ↓
Decision:
   ├── Normal Chat
   └── Tool Call
          ↓
     ToolNode
   ├── Stock Price
   ├── Buy (HITL)
   ├── Sell (HITL + Validation)
   └── Portfolio
          ↓
LLM Response
          ↓
UI Display
```

---

## 📂 Project Structure

```plaintext
.
├── backend.py        # LangGraph + Tools + HITL logic
├── app.py           # Streamlit UI
├── .env             # API keys
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/maheshmsgowda58/langgraph-chatbot-with-hitl.git
cd langgraph-chatbot-with-hitl
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

OR (using uv)

```bash
uv add -r requirements.txt
```

---

## 🔑 Environment Setup

Create `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 🧪 Example Queries

### 💬 General Chat

* "What is AI?"
* "Explain machine learning"

---

### 📈 Stock Queries

* "What is the price of AAPL?"
* "Show Tesla stock price"

---

### 💰 Buy Stock

* "Buy 10 shares of AAPL"
  → 🔔 HITL popup appears

---

### 📉 Sell Stock

* "Sell 5 shares of AAPL"
  → 🔔 HITL popup appears

---

### 📊 Portfolio

* "Show my portfolio"

---

## ⚠️ Important Notes

* Portfolio is stored **in-memory (temporary)**
* Restarting app resets data
* HITL required for buy/sell operations
* Ensure valid stock symbols

---

## 🚀 Future Improvements

* 💾 Database persistence (save portfolio)
* 📊 Profit/Loss tracking
* 📈 Stock charts visualization
* 🔍 LangSmith tracing
* 🤖 Multi-agent system
* 🌐 Deployment (Streamlit Cloud / AWS)

---

## 🧠 Tech Stack

* LangGraph
* LangChain
* Groq (LLM)
* Streamlit
* Python

---

## ⭐ Final Note

This project demonstrates a **production-level Agentic AI system** combining:

* LLM reasoning
* Tool execution
* Human-in-the-loop safety
* Stateful workflow (LangGraph)

👉 You are now building **real-world AI systems** 🚀
