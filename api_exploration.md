# S&F API Exploration Guide

## API Structure

Base pattern:
```
https://{server}.sfgame.eu/cmd.php?req={Command}&params={base64_params}&sid={session_id}
```

## Known Endpoints

### Example: PlayerAttributIncrease
```
https://s17.sfgame.eu/cmd.php?req=PlayerAttributIncrease&params=MS8w&sid=0-83TiJwzb2r8lF4
```
- **Decoded params**: `1/0`
- **Purpose**: Increase player attribute
- **Format**: `{attribute_id}/{amount}`

### To Discover More:

1. Open browser DevTools (F12) → Network tab
2. Filter by "cmd.php"
3. Perform actions in game:
   - Login
   - View character equipment
   - View other players
   - Start battles
   - Open scrapbook
   - Browse hall of fame
4. Document each call:
   - Command name
   - Decoded params
   - Response format

### Commands to Look For:

Based on the scrapbook-helper functionality:

- **Login/Auth**: Initial authentication
- **PlayerProfile**: Get player equipment/stats
- **HallOfFame**: Browse HOF pages
- **Scrapbook**: View scrapbook items
- **Attack/Battle**: Combat commands
- **Update**: Periodic state updates

## Response Format

Responses are likely JSON containing:
- Success/error status
- Updated game state
- Command results

## Important Notes

⚠️ **Rate Limiting**: S&F has rate limiting in place
⚠️ **ToS Compliance**: Check if automated access is allowed
⚠️ **Respectful Usage**: Don't hammer the servers
