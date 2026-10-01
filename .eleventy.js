module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("img");
  return {
    dir: {
      input: ".",
      output: "_site"
    }
  };
};
