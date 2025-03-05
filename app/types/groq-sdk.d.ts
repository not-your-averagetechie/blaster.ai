declare module 'groq-sdk' {
  export class Groq {
    constructor(config: { apiKey: string });
    chat: {
      completions: {
        create(params: {
          messages: Array<{ role: string; content: string }>;
          model: string;
        }): Promise<{
          choices: Array<{
            message?: {
              content: string;
            };
          }>;
        }>;
      };
    };
  }
}
