import { ChatGroq } from 'langchain/chat_models/groq';
import { HumanMessage } from 'langchain/schema';

const MODEL_NAME = 'llama-3.3-70b-versatile';

export async function makeGroqRequest(prompt: string) {
  try {
    console.log(`Using LangChain with model: ${MODEL_NAME}`);

    const chat = new ChatGroq({
      apiKey: process.env.GROQ_API_KEY,
      modelName: MODEL_NAME,
      temperature: 0.7,
    });

    const response = await chat.call([
      new HumanMessage(prompt),
    ]);

    return response.content;
  } catch (error) {
    console.error("LangChain Groq error:", error);
    throw error;
  }
}
