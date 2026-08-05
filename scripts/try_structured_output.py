from cli_ai_agent.structured import classify_request

result = classify_request( "What is the weather in Bucharest today?" )
print( result.model_dump_json( indent = 2 ) )