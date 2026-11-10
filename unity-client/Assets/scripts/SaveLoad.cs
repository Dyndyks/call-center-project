using System.IO;
using UnityEngine;

public class SaveLoad : MonoBehaviour
{
    private string savepath;

    void Awake()
    {
        savepath = System.IO.Path.Combine(Application.persistentDataPath, "saveuser.json");
    }


    public void SaveUser(int id, string name)
    {
        User data = new User
        {
            user_id = id,
            user_name = name,
        };
        string json = JsonUtility.ToJson(data);
        File.WriteAllText(savepath, json);
        

    }


    public User LoadUser()
    {
        if (File.Exists(savepath))
        {
            string json = File.ReadAllText(savepath);
            return JsonUtility.FromJson<User>(json);
        }
        return null;
    }
}

[System.Serializable]
public class User
{
    public int user_id;
    public string user_name;
}
