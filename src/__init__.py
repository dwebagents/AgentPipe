// src/generate_issues_v1_0.ts
import { generateIssues, Issues } from './generate_issue_generator';

export const issues: Issue[] = await generateIssues({
  repositoryPath: 'src',
  titleFormat: (title) => `${title} - [Bounty] Jackpot`,
});

export default issues;
