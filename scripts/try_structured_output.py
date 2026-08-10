from cli_ai_agent.structured import classify_request

result = classify_request( "How many people live in Bucharest currently?" )
print( result.model_dump_json( indent = 2 ) )