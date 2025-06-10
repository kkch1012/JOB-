from fastapi import FastAPI
from routers import auth, users, recommend, roadmap, community,job_postings
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(job_postings.router, prefix="/jobs", tags=["Jobs"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(roadmap.router, prefix="/roadmap", tags=["Roadmap"])
app.include_router(community.router, prefix="/community", tags=["Community"])