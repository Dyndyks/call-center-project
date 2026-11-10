using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.Collections;
using System.Text;

public class GetName : MonoBehaviour
{
    public TMP_InputField nameInput;
    public SaveLoad saveload;
    public GameObject namebutton;
    public GameObject menubutton;

    public void SendName()
    {
        string name = nameInput.text;
        StartCoroutine(SendRequst(name));
        namebutton.SetActive(false);
        menubutton.SetActive(true);
    }

    IEnumerator SendRequst(string name)
    {
        string url = "http://127.0.0.1:8000/user";

        var data = new UserCreate { name = name };
        string json = JsonUtility.ToJson(data);
        byte[] body = Encoding.UTF8.GetBytes(json);


        using UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(body);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            var response = JsonUtility.FromJson<UserResponse>(request.downloadHandler.text);
            int user_id = response.user_id;
            saveload.SaveUser(user_id, response.user_name);

        }
        else
        {
            Debug.Log("no");
        }
    }
}

public class UserCreate
{
    public string name;
}

[System.Serializable]
public class UserResponse
{
    public int user_id;
    public string user_name;
}
