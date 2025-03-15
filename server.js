const express = require('express');
const cors = require('cors');
const { Groq } = require('groq-sdk');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3001;

// Validate environment variables
if (!process.env.GROQ_API_KEY) {
  console.error('ERROR: GROQ_API_KEY is not set in .env file');
  process.exit(1);
}

// Initialize Groq client
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

app.use(cors({
  origin: ['http://localhost:3000', 'http://localhost:3001'],
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

app.use(express.json());

async function processWithGroq(messages) {
  try {
    console.log('Making Groq API call with messages:', JSON.stringify(messages, null, 2));
    const completion = await groq.chat.completions.create({
      messages,
      model: "mixtral-8x7b-32768",
      temperature: 0.7,
      max_tokens: 2048,
    });
    console.log('Received response from Groq:', completion.choices[0]?.message?.content);
    return completion.choices[0]?.message?.content || "Sorry, I couldn't process that.";
  } catch (error) {
    console.error('Error in processWithGroq:', error);
    if (error.response) {
      console.error('API Response:', error.response.data);
    }
    throw new Error(`Groq API Error: ${error.message}`);
  }
}

// Test endpoint to verify Groq connection
app.get('/api/test', async (req, res) => {
  try {
    const response = await processWithGroq([
      {
        role: "user",
        content: "Hello, this is a test message."
      }
    ]);
    res.json({ success: true, message: response });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message,
      details: 'Failed to connect to Groq API'
    });
  }
});

// Task handler endpoint
app.post('/api/task', async (req, res) => {
  try {
    const { task, text } = req.body;

    if (!task || !text) {
      return res.status(400).json({ error: 'Task and text are required' });
    }

    let mainResult, refinementResult, validationResult;
    
    // Step 1: Main Task Processing
    switch (task) {
      case 'Summarize Medical Text':
        mainResult = await processWithGroq([
          {
            role: "system",
            content: "You are a medical professional tasked with summarizing complex medical texts. Provide clear, accurate, and concise summaries while maintaining all important medical information."
          },
          {
            role: "user",
            content: `Please summarize the following medical text:\n\n${text}`
          }
        ]);

        // Refinement
        refinementResult = await processWithGroq([
          {
            role: "system",
            content: "You are an expert editor who refines and enhances content for clarity, coherence, and quality. Focus on improving medical summaries while maintaining accuracy."
          },
          {
            role: "user",
            content: `Please refine the following medical summary to improve its clarity, coherence, and overall quality:\n\n${mainResult}\n\nRefined Summary:`
          }
        ]);

        // Validation
        validationResult = await processWithGroq([
          {
            role: "system",
            content: "You are an AI assistant that validates summaries of medical texts for accuracy, completeness, and conciseness."
          },
          {
            role: "user",
            content: `Assess the given summary against the original text based on the following criteria:
- **Accuracy** (Does the summary correctly represent key points?)
- **Conciseness** (Is the summary brief but informative?)
- **Relevance** (Does it exclude unnecessary details while covering the main ideas?)

Provide structured feedback on each aspect and an **overall rating (1-5)**, where **5** indicates an excellent summary.

**Original Text:**
${text}

**Initial Summary:**
${mainResult}

**Refined Summary:**
${refinementResult}

**Summary Validation Report:**`
          }
        ]);
        break;

      case 'Write and Refine Research Article':
        mainResult = await processWithGroq([
          {
            role: "system",
            content: "You are a scientific writer specializing in research articles. Write clear, well-structured academic content."
          },
          {
            role: "user",
            content: `Write a research article based on the following topic and outline:\n\n${text}`
          }
        ]);

        // Refinement
        refinementResult = await processWithGroq([
          {
            role: "system",
            content: "You are an expert editor who refines and enhances research articles for clarity, coherence, and academic quality."
          },
          {
            role: "user",
            content: `Please refine the following research article draft to improve its language, coherence, and overall quality:\n\n${mainResult}\n\nRefined Article:`
          }
        ]);

        // Validation
        validationResult = await processWithGroq([
          {
            role: "system",
            content: "You are an academic peer reviewer. Validate research articles for academic quality, methodology, and clarity."
          },
          {
            role: "user",
            content: `Review this research article for academic quality, methodology, and clarity. Provide structured feedback:

**Original Topic/Outline:**
${text}

**Initial Draft:**
${mainResult}

**Refined Article:**
${refinementResult}

**Peer Review Report:**`
          }
        ]);
        break;

      case 'Sanitize Medical Data (PHI)':
        mainResult = await processWithGroq([
          {
            role: "system",
            content: "You are a healthcare data privacy expert. Remove all Protected Health Information (PHI) while maintaining medical relevance."
          },
          {
            role: "user",
            content: `Sanitize the following medical data by removing all PHI:\n\n${text}`
          }
        ]);

        // Refinement
        refinementResult = await processWithGroq([
          {
            role: "system",
            content: "You are an expert editor who refines and enhances sanitized medical data. Improve clarity while ensuring all PHI remains removed."
          },
          {
            role: "user",
            content: `Please refine the following sanitized medical data to improve its clarity and readability while maintaining PHI removal:\n\n${mainResult}\n\nRefined Sanitized Data:`
          }
        ]);

        // Validation
        validationResult = await processWithGroq([
          {
            role: "system",
            content: "You are a HIPAA compliance officer. Verify that all PHI has been properly removed from medical data."
          },
          {
            role: "user",
            content: `Verify that all PHI has been properly removed from this sanitized text. Check for any remaining identifiable information:

**Original Text:**
${text}

**Initial Sanitized Text:**
${mainResult}

**Refined Sanitized Text:**
${refinementResult}

**HIPAA Compliance Report:**`
          }
        ]);
        break;

      default:
        return res.status(400).json({ error: 'Invalid task type' });
    }

    res.json({
      mainResult,
      refinementResult,
      validationResult
    });
    
  } catch (error) {
    console.error('Error in /api/task:', error);
    res.status(500).json({ 
      error: 'Failed to process task',
      details: error.message 
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`GROQ_API_KEY ${process.env.GROQ_API_KEY ? 'is' : 'is NOT'} set`);
}); 