# S&F Password Hashing Mechanism

## Overview

The Shakes & Fidget API uses **SHA-1 hashing** with a **fixed salt constant** for password authentication.

## Algorithm Details

### Step-by-Step Process

1. **Concatenate**: `password + HASH_CONST`
2. **Hash**: SHA-1 hash of the concatenated string
3. **Format**: Lowercase hexadecimal representation

### Hash Constant

```
HASH_CONST = "ahHoj2woo1eeChiech6ohphoB7Aithoh"
```

This is a fixed salt value used by the game's authentication system.

### Rust Implementation (from sf-api)

```rust
pub const HASH_CONST: &str = "ahHoj2woo1eeChiech6ohphoB7Aithoh";

pub fn sha1_hash(val: &str) -> String {
    use sha1::{Digest, Sha1};
    let mut hasher = Sha1::new();
    hasher.update(val.as_bytes());
    let hash = hasher.finalize();
    let mut result = String::with_capacity(hash.len() * 2);
    for byte in &hash {
        _ = result.write_fmt(format_args!("{byte:02x}"));
    }
    result
}

// Usage:
impl PWHash {
    pub fn new(password: &str) -> Self {
        Self(sha1_hash(&(password.to_string() + HASH_CONST)))
    }
}
```

## Python Implementation

```python
import hashlib

HASH_CONST = "ahHoj2woo1eeChiech6ohphoB7Aithoh"

def hash_password(password: str) -> str:
    """
    Hash password using S&F's SHA-1 + constant method

    Args:
        password: Plain text password

    Returns:
        SHA-1 hash in lowercase hexadecimal format
    """
    # Concatenate password with constant
    salted = password + HASH_CONST

    # Compute SHA-1 hash
    hasher = hashlib.sha1()
    hasher.update(salted.encode('utf-8'))

    # Return lowercase hexadecimal digest
    return hasher.hexdigest()

# Example usage:
password = "mypassword123"
hashed = hash_password(password)
print(f"Password: {password}")
print(f"Hashed:   {hashed}")
```

## Example

```python
>>> hash_password("test")
'5f3a38a7657c20f2c3ba4d95e51ad50e22cf27e0'
```

## Security Notes

⚠️ **Security Concerns:**

1. **SHA-1 is deprecated** - Known to be cryptographically weak
2. **Fixed salt** - The same constant is used for all passwords
3. **Client-side hashing** - While better than sending plaintext, it's not as secure as modern methods
4. **No per-user salt** - All users use the same hash constant

This is an older authentication scheme. Modern applications should use:
- Argon2id, bcrypt, or PBKDF2
- Per-user salts
- Server-side hashing
- Proper rate limiting

However, since this is the game's protocol, we must use their method to authenticate.

## How Password is Sent

When logging in, the API call looks like:

```
POST https://s17.sfgame.eu/cmd.php
req=Login
params={base64_encoded_username}/{base64_encoded_password_hash}
```

The password hash (not plain password) is sent in the params after base64 encoding.

## Integration with Python Client

```python
def login(username: str, password: str, server: str) -> dict:
    """Login to S&F server"""
    # Hash the password
    pw_hash = hash_password(password)

    # Encode parameters
    params = base64.b64encode(f"{username}/{pw_hash}".encode()).decode()

    # Make request
    url = f"https://{server}/cmd.php?req=Login&params={params}"
    response = requests.get(url)

    return response.json()
```
