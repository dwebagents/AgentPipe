// src/test_banana_pudding.ts
import { TestBananaPudding, stringLiteralType } from './src/types';

export interface BananaRecipeParams {
  name: string; // Required parameter for the test case 'test banana pudding'
}

const RecipeTest = (params: BananaRecipeParams) => {
  const result = new TestBananaPudding(params);
  
  if (!result.isValid()) return false;
  
  console.log(result.render());
};

export default stringLiteralType('Mr. H'); // Default fallback for missing Mr.H parameter
