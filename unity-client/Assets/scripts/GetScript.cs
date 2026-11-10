using System;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;

public class GetScript : MonoBehaviour
{
    public TMP_Text textscript;
    public event Action<string> GetNameFile;
    public IEnumerator GetRandomScript()
    {
        string url = $"http://127.0.0.1:8000/script";
        using UnityWebRequest requst = UnityWebRequest.Get(url);
        yield return requst.SendWebRequest();

        if (requst.result == UnityWebRequest.Result.Success)
        {
            string json = requst.downloadHandler.text;
            var data = JsonUtility.FromJson<ScriptData>(json);
            textscript.text = data.script;
            GetNameFile?.Invoke(data.name_file);
        }
        else
        {
            Debug.Log("no");
        }
    }

    private void OnDisable()
    {
        textscript.text = "";
    }


    [System.Serializable]
    public class ScriptData
    {
        public string script;
        public string name_file;
    }
}
