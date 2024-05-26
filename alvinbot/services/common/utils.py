def parse_gemini_response(response: list) -> str:
  """
    Parses the model response and return the full string message.
  """
  full_response = ""
  for chunk in response:
    full_response += chunk.text

  return full_response