
import sys
sys.path.insert(0, '../services_utils')
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List
from config import GITHUB_AUTH_TOKEN
from db import SessionLocal, engine
import concurrent.futures
import models
import schemas
import requests
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GitHub Events API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch star count from GitHub API
def get_repo_star_count(repo_name: str) -> int:
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {}
    if GITHUB_AUTH_TOKEN:
        headers['Authorization'] = f"token {GITHUB_AUTH_TOKEN}"
    try: 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("stargazers_count", 0)
        else:
            return 0
    except Exception as e:
        print(f"Error fetching star count for repo {repo_name}: {e}")
        return 0


@app.get("/events/", response_model=List[schemas.EventSchema])
def list_events(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    
    events_with_actors_and_repos = (
        db.query(models.Event)
        .options(
            joinedload(models.Event.actor),      # Eager load the Actor relationship
            joinedload(models.Event.repository)  # Eager load the Repository relationship
        )
        .order_by(desc(models.Event.id))         
        .offset(skip)
        .limit(limit)
        .all()
    )


    # Fetch star counts for each repository concurrently using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # list of repo names to fetch star count for, only if the star count is not already present
        repo_names = [event.repository.name for event in events_with_actors_and_repos if not event.repository.stars and event.repository.stars != 0]
        # make repo_names unique
        repo_names = list(set(repo_names))
        futures = {executor.submit(get_repo_star_count, repo_name): event for repo_name, event in zip(repo_names, events_with_actors_and_repos)}
        print(len(futures))
        for future in concurrent.futures.as_completed(futures):
            event = futures[future]
            try:
                event.repository.stars = future.result()
            except Exception as e:
                print(f"Error fetching star count for repo {event.repository.name}: {e}")

    db.commit()

    return events_with_actors_and_repos

@app.get("/events/count")
def count_events(db: Session = Depends(get_db)):
    count = db.query(models.Event).count()
    return {"total_events": count}

@app.get("/actors/recent", response_model=List[schemas.ActorSchema])
def list_recent_actors(db: Session = Depends(get_db)):
    subquery = db.query(
        models.Event.actor_id,
        models.Event.created_at
    ).order_by(models.Event.created_at.desc()).distinct(models.Event.actor_id).limit(20).subquery()

    actors = db.query(models.Actor).join(
        subquery, models.Actor.id == subquery.c.actor_id
    ).order_by(subquery.c.created_at.desc()).all()

    return actors

@app.get("/repositories/recent", response_model=List[schemas.RepositorySchema])
def list_recent_repositories(db: Session = Depends(get_db)):
    subquery = db.query(
        models.Event.repo_id,
        models.Event.created_at
    ).order_by(models.Event.created_at.desc()).distinct(models.Event.repo_id).limit(20).subquery()

    repositories = db.query(models.Repository).join(
        subquery, models.Repository.id == subquery.c.repo_id
    ).order_by(subquery.c.created_at.desc()).all()

    # Fetch star counts for each repository
    # for repo in repositories:
    #     if not repo.stars and repo.stars != 0:
    #         repo.stars = get_repo_star_count(repo.name)
        
    # Fetch star counts for each repository concurrently using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # list of repo names to fetch star count for, only if the star count is not already present
        repo_names = [repo.name for repo in repositories if not repo.stars and repo.stars != 0]
        futures = {executor.submit(get_repo_star_count, repo_name): repo for repo_name, repo in zip(repo_names, repositories)}
        
        for future in concurrent.futures.as_completed(futures):
            repo = futures[future]
            try:
                print(f"Fetching star count for repo {repo.name}")
                repo.stars = future.result()
            except Exception as e:
                print(f"Error fetching star count for repo {repo.name}: {e}")

    # save the db the stars
    db.commit()

    return repositories
