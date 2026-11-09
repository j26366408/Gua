(function (root) {
  function grade(results, systemWorks = true) {
    if (!Array.isArray(results) || results.length !== 4 || results.some(x => typeof x !== 'boolean')) {
      throw new TypeError('Exactly four boolean results are required.');
    }
    const questions = results.map(x => x ? 20 : 0);
    const fifth = systemWorks ? 20 : 0;
    return { questions, fifth, total: questions.reduce((a, b) => a + b, 0) + fifth };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { grade };
  root.achievementGrade = grade;
})(typeof window !== 'undefined' ? window : globalThis);
