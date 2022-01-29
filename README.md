## mini app for comment moderation

###### Project testing on Ubuntu 20.04

### How to setting
 - Create a new virtual environment:
```
python3 -m venv miniapp_env
```
 - And activate it:
```
source miniapp_env/bin/activate
```
 - Update pip:
```
python3 -m pip install --upgrade pip
```
 - Clone repository:
```
git clone this repository
```
- Install project requirements:
```
cd mini_app
pip3 install -r requirements.txt
```

### How to start

```
python3 utils/server.py         
```

### Рow to test the algorithm

##### Open new terminal, activate v_env and run command:
```
python3 utils/client.py         
```
