/**
 * Common interfaces and types used throughout the application
 */

/**
 * API response format for general messages
 */
export interface ApiResponse {
  message: string;
}

/**
 * API error response format
 */
export interface ApiError {
  detail: string;
}
