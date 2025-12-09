// Sample JavaScript file with various code quality issues

function processUserData(userData) {
  // This is a long function that does too many things
  const password = "hardcoded123"; // Security issue!
  const apiKey = "sk-1234567890abcdef"; // Another security issue!
  
  console.log("Processing user:", userData);
  console.log("Step 1");
  console.log("Step 2");
  console.log("Step 3");
  console.log("Step 4");
  console.log("Step 5");
  console.log("Step 6");
  
  // TODO: Fix this later
  // FIXME: This is broken
  
  if (userData && userData.name && userData.email && userData.age && userData.address && userData.phone) {
    if (userData.age > 18 && userData.age < 65 && userData.verified === true || userData.premium === true) {
      if (userData.country === "US" || userData.country === "UK" || userData.country === "CA") {
        document.getElementById("user-info").innerHTML = userData.name; // XSS vulnerability!
        
        // Magic numbers everywhere
        const result = userData.score * 42 + 137 - 256;
        const another = result / 999 + 12345;
        
        try {
          eval(userData.customCode); // Very dangerous!
        } catch (e) {
          // Empty catch block
        }
        
        for (let i = 0; i < 100; i++) {
          if (i % 2 === 0) {
            if (i % 3 === 0) {
              if (i % 5 === 0) {
                console.log(i);
              }
            }
          }
        }
        
        return true;
      }
    }
  }
  return false;
}

function anotherVeryLongLineOfCodeThatExceedsTheRecommendedLineLengthAndShouldBeRefactoredIntoSmallerPiecesForBetterReadability() {
  return "This line is way too long and violates coding standards";
}

const user = {
  name: "John",
  password: "admin123"
};
