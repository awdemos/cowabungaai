import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './fileHelpers';
import { deleteAllAssistants } from './assistantHelpers';
import { deleteAllThreads } from './threadHelpers';
import type OpenAI from 'openai';
import { deleteAllTestAPIKeys } from './apiHelpers';

export const cleanup = async (openAIClient: OpenAI) => {
  deleteAllGeneratedFixtureFiles();
  await deleteAllThreads(openAIClient);
  await deleteAllAssistants(openAIClient);
  await deleteAllTestFilesWithApi(openAIClient);
  await deleteAllTestAPIKeys();
};
