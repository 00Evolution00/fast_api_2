import sys
sys.path.append('src')
from services.auth import AuthService
from schemas.auth import RegisterRequest
from core.db import database
import asyncio


async def test_register():
    async with database.session() as db:
        auth_service = AuthService(db)
        try:
            result = await auth_service.register(RegisterRequest(
                first_name='Test',
                last_name='User',
                username='testuser',
                email='test@example.com',
                password='TestPassword123!'
            ))
            print(f'Registration result: {result}')
        except Exception as e:
            print(f'Registration error: {e}')


async def main():
    await test_register()


if __name__ == '__main__':
    asyncio.run(main())
