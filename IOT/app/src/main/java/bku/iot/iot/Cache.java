package bku.iot.iot;

import java.util.HashMap;

public class Cache {

    private static Cache instance;
    private HashMap<String, Object> dataCache;

    private Cache() {
        dataCache = new HashMap<>();
    }

    public static synchronized Cache getInstance() {
        if (instance == null) {
            instance = new Cache();
        }
        return instance;
    }

    public void putData(String key, Object data) {
        dataCache.put(key, data);
    }

    public Object getData(String key) {
        return dataCache.get(key);
    }

    public void removeData(String key) {
        dataCache.remove(key);
    }

    public void clearCache() {
        dataCache.clear();
    }
}
