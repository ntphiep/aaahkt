/**
 * Sample JavaScript file with good code practices
 * This demonstrates clean, maintainable code
 */

const USER_MIN_AGE = 18;
const USER_MAX_AGE = 65;
const SCORE_MULTIPLIER = 42;

/**
 * Validates user data
 * @param {Object} userData - User data object
 * @returns {boolean} True if valid, false otherwise
 */
function validateUserData(userData) {
  if (!userData) {
    return false;
  }
  
  return userData.name && 
         userData.email && 
         userData.age &&
         userData.address;
}

/**
 * Checks if user meets age requirements
 * @param {number} age - User's age
 * @returns {boolean} True if age is valid
 */
function isValidAge(age) {
  return age >= USER_MIN_AGE && age <= USER_MAX_AGE;
}

/**
 * Processes user data safely
 * @param {Object} userData - User data object
 * @returns {boolean} True if processing succeeded
 */
function processUserData(userData) {
  if (!validateUserData(userData)) {
    return false;
  }
  
  if (!isValidAge(userData.age)) {
    return false;
  }
  
  // Use textContent instead of innerHTML for security
  const userInfoElement = document.getElementById("user-info");
  if (userInfoElement) {
    userInfoElement.textContent = sanitizeText(userData.name);
  }
  
  return true;
}

/**
 * Sanitizes text input to prevent XSS
 * @param {string} text - Input text
 * @returns {string} Sanitized text
 */
function sanitizeText(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

export { processUserData, validateUserData, isValidAge };
