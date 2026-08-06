from cli_ai_agent.structured import classify_request

result = classify_request( "Explain to me how timetables work." )
print( result.model_dump_json( indent = 2 ) )