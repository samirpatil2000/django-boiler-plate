from contextvars import ContextVar

# Define context variables
request_var = ContextVar("request", default=None)
trace_id_var = ContextVar("trace_id", default=None)
user_id_var = ContextVar("user_id", default=None)
tenant_id_var = ContextVar("tenant_id", default=None)
