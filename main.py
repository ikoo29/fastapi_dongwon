import os
from fastapi import FastAPI, Request
from databases import Database

app = FastAPI()

# 환경변수에서 데이터베이스 설정 읽기
DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 데이터베이스 URL 구성
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()

# Database 객체 생성
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/webhook/")
async def get_property_details(request: Request):
    # 요청 JSON 데이터를 파이썬 객체로 변환
    data = await request.json()
    # 변수들 추출
    customer_status = data['action']['detailParams']['customer_status']['origin']
    property_type = data['action']['detailParams']['property_type']['origin']
    address = data['action']['detailParams']['address']['origin']
    move_in_date = data['action']['detailParams']['move_in_date']['origin']
    deposit_and_rent = data['action']['detailParams']['deposit_and_rent']['origin']
    maintenance_detail = data['action']['detailParams']['maintenance_detail']['origin']
    visit_times = data['action']['detailParams']['visit_times']['origin']
    contact_number = data['action']['detailParams']['contact_number']['origin']
    # 모든 정보를 반환
    return {
        "road": road,
        "num": num,
        "full_address": full_address,
        "customer_status": customer_status,
        "property_type": property_type,
        "address": address,
        "move_in_date": move_in_date,
        "deposit_and_rent": deposit_and_rent,
        "maintenance_detail": maintenance_detail,
        "visit_times": visit_times,
        "contact_number": contact_number
    }


@app.post("/add-contact")
async def add_contact():
    query = """
    INSERT INTO "test-table" ("이름", "주소", "전화번호")
    VALUES ('박기자', '중동', '010-2959-1111');
    """
    await database.execute(query)
    return {"status": "Contact added successfully"}
