// src/utils/object_utils.js

/**
 * Safely retrieves a nested property from an object using a dot-separated path.
 * Returns undefined if any part of the path does not exist.
 *
 * @param {object} obj The object to traverse.
 * @param {string} path The dot-separated path to the desired property (e.g., "user.address.street").
 * @param {*} [defaultValue] The value to return if the property is not found.
 * @returns {*} The value of the nested property, or undefined if not found, or defaultValue if provided.
 */
export function getNestedProperty(obj, path, defaultValue) {
  if (!obj || typeof obj !== 'object' || obj === null) {
    return defaultValue !== undefined ? defaultValue : undefined;
  }

  const parts = path.split('.');
  let current = obj;

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (current === null || typeof current !== 'object' || !current.hasOwnProperty(part)) {
      return defaultValue !== undefined ? defaultValue : undefined;
    }
    current = current[part];
  }

  return current !== undefined ? current : (defaultValue !== undefined ? defaultValue : undefined);
}