
Here's the text content from the image, which appears to be a coding style guide for comments:

1. **Comment With Purpose**
- Only include comments that add value to the code. Avoid redundant or self-explanatory comments.
- ✓ Good: "# Using binary search for better performance on large datasets"
- ✗ Bad: "# This adds two numbers" for 'a + b'

2. **Avoid Noise**
- Do not clutter the code with unnecessary comments. Comments should clarify, not distract. If the code is clear, no comment is needed.

3. **Focus on the "Why"**
- Comments should explain *why* something is done, not *what* the code does (the code itself should be self-explanatory).
- ✓ Good: "# Using binary search for better performance on large datasets"
- ✗ Bad: "# Loop through the array"

4. **Keep Comments Up-to-Date**
- Outdated comments are worse than no comments. Always update or remove comments when the code changes.

5. **Avoid Commenting Out Code**
- Do not leave large blocks of commented out code in the repository. Use version control (e.g., Git) to track old code instead.

6. **Use TODOs Sparingly**
- Only include 'TODO' comments for actionable items that will be addressed soon. Include a date and ticket reference for tracking:
- ✓ Good: "# TODO [ARES-1234] [2024-10-17]: Refactor this method to use the new API endpoint"
- ✓ Good: "# TODO: Remove deprecated feature after Q1 2025 migration (ARES-5678)"
- ✗ Bad: "# TODO: Fix this later"
- ✗ Bad: "# TODO: Optimize performance"
- Avoid leaving long-term or vague TODOs in the codebase.

7. **Be Professional**
- Comments should be clear, concise, and professional. Avoid jokes, irrelevant remarks, or personal notes.

8. **Document Complex Logic**
- If the code involves complex logic, edge cases, or workarounds, include a comment explaining the reasoning.
