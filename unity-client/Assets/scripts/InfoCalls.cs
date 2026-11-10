using UnityEngine;
using TMPro;
using System.Collections;
using UnityEngine.Networking;
using UnityEngine.InputSystem.Controls;

public class InfoCalls : MonoBehaviour
{
    public SaveLoad saveload;
    public TMP_Text statstext;

    private void OnEnable()
    {
        User userdata = saveload.LoadUser();
        StartCoroutine(GetAllStats(userdata.user_id));
    }


    IEnumerator GetAllStats(int user_id)
    {
        string url = $"http://127.0.0.1:8000/stats?user_id={user_id}";
        using UnityWebRequest requst = UnityWebRequest.Get(url);
        yield return requst.SendWebRequest();

        if (requst.result == UnityWebRequest.Result.Success)
        {
            string json = requst.downloadHandler.text;
            var response = JsonUtility.FromJson<StatsData>(json);
            statstext.text = $"-----------------\nКол-во: {response.calls.ToString()}\nУспешные: {response.succ_calls.ToString()}";
        }
        else
        {
            Debug.Log("no");
        }
    }

    [System.Serializable]
    public class StatsData
    {
        public int calls;
        public int succ_calls;
    }

}
