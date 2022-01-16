# Notify Mirror
Wip android to linux notification mirroring client that supports custom notification actions. Pushbullet is the service used to fetch the android notifications.

## Running
1. Get a pushbullet api key
2. Create a config file that looks like `example-config.ini`
3. Run `main.py` 

## Notification actions
To create a notificaion action on click create a new section from the package name and set the exec_on_click option.

```
[com.test]
exec_on_click = bash -c "notify-send test" 
```
