# FastAPI Exercise: PATCH and DELETE Endpoints with MongoDB

This project demonstrates the implementation of PATCH and DELETE endpoints for a FastAPI application that interfaces with MongoDB using the Motor driver.

### Person Model

The `Person` model is defined as follows:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    occupation: str
    address: str
```

### Summary

This tutorial show the use of PATCH and DELETE HTTP methods with FastAPI and MongoDB. The routes
```jsx
PATCH "/persons/{person_id}"
DELETE "/persons/{person_id}"
```

Patch was implemented using the `update_one()` method and `$set` operator from the MongoDB driver and Delete was implemented using the `delete_one()` method.

String IDs are always converted to `ObjectId` before querying MongoDB. This conversion is necessary because MongoDB uses `ObjectId` for its document IDs.

## Testing

Endpoints are tested using Postman.

<aside>
💡Errors are handled appropriately and input data is validated.
</aside>

## Dependencies

The project dependencies are listed in `requirements.txt` for first-level dependencies and `requirements.lock` for specific versions.
