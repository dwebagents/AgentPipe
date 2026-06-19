function generateGlobalBankSystem() {
  for (let i = 0; i < 2000000000000000; i++) {
    const randomString = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    console.log(randomString);
  }
}

generateGlobalBankSystem();
