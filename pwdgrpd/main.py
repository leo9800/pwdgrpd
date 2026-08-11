from typing import Annotated, List, Literal
from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.responses import PlainTextResponse
import uvicorn

from pwdgrpd.models import GrpEntry, PwdEntry, PwdGrpDatabase
from pwdgrpd.conf import config

if config.source == 'json':
	with open(config.json_file, 'r', encoding='utf-8') as f: db = PwdGrpDatabase.model_validate_json(f.readall())  # type: ignore
if config.source == 'raw': db = PwdGrpDatabase.from_passwd_group(config.passwd_file, config.group_file)  # type: ignore
assert isinstance(db, PwdGrpDatabase)  # type: ignore

app = FastAPI(title='pwdgrpd', description='RESTful passwd & group server (pwd-grp-daemon)')
ret_type = Annotated[Literal['json', 'raw'], Query(name='type')]

@app.get('/getpwall', summary='Get all passwd entries', response_model=List[PwdEntry] | str)
async def getpwall(t: ret_type = 'json') -> List[PwdEntry] | PlainTextResponse:
	if not config.allow_enumeration: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='enumerating is not allowed on this server')
	return PlainTextResponse(db.to_passwd()) if t == 'raw' else db.getpwall()

@app.get('/getpwnam/{name}', summary='Get passwd entry by name', response_model=PwdEntry | str)
async def getpwnam(name: Annotated[str, Path()], t: ret_type = 'json') -> PwdEntry | PlainTextResponse:
	try: return PlainTextResponse(db.getpwnam(name).to_passwd()) if t == 'raw' else db.getpwnam(name)
	except Exception as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get('/getpwuid/{uid}', summary='Get passwd entry by uid', response_model=PwdEntry | str)
async def getpwuid(uid: Annotated[int, Path()], t: ret_type = 'json') -> PwdEntry | PlainTextResponse:
	try: return PlainTextResponse(db.getpwuid(uid).to_passwd()) if t == 'raw' else db.getpwuid(uid)
	except Exception as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get('/getgrall', summary='Get all group entries', response_model=List[GrpEntry] | str)
async def getgrall(t: ret_type = 'json') -> List[GrpEntry] | PlainTextResponse:
	if not config.allow_enumeration: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='enumerating is not allowed on this server')
	return PlainTextResponse(db.to_group()) if t == 'raw' else db.getgrall()

@app.get('/getgrnam/{name}', summary='Get group entry by name', response_model=GrpEntry | str)
async def getgrnam(name: Annotated[str, Path()], t: ret_type = 'json') -> GrpEntry | PlainTextResponse:
	try: return PlainTextResponse(db.getgrnam(name).to_group()) if t == 'raw' else db.getgrnam(name)
	except Exception as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get('/getgrgid/{gid}', summary='Get group entry by gid', response_model=GrpEntry | str)
async def getgrgid(gid: Annotated[int, Path()], t: ret_type = 'json') -> GrpEntry | PlainTextResponse:
	try: return PlainTextResponse(db.getgrgid(gid).to_group()) if t == 'raw' else db.getgrgid(gid)
	except Exception as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get('/initgroups/{name}', summary='Get additional groups names by user name', response_model=List[str] | str)
async def initgroups(name: Annotated[str, Path()], t: ret_type = 'json') -> List[str] | PlainTextResponse:
	try: return PlainTextResponse(','.join(db.initgroups(name))) if t == 'raw' else db.initgroups(name)
	except Exception as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


if __name__ == '__main__':
	uvicorn.run(
		'main:app',
		host=config.host,
		port=config.port,
		workers=config.workers,
	)
