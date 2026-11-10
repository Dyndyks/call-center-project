using TMPro;
using UnityEngine;
using System.Text.RegularExpressions;
using System;

public class OperationCall : MonoBehaviour
{
    public GetScript getscript;
    public EndCall endcall;
    public GameObject exitcallbutton;
    public GameObject exitbutton;
    public Web web;
    public Micro micro;
    public SaveLoad saveload;
    public TMP_Text sub;
    public TMP_Text callsuccestext;
    public TMP_Text timetheendtext;
    public float timeend = 120f;
    private bool checkconnect = false;
    private string file;

    async void OnEnable()
    {
        StartCoroutine(getscript.GetRandomScript());
        ExitOnOff(true, false);
        timeend = 120f;
        endcall.OnCallEnded += HandleEndCall;

        getscript.GetNameFile += SendNameFile;
        web.OnConnected += OnServer;
        web.OnMessageReceveid += HandleText;
        await web.ConnectToServer();
    }

    void Update()
    {
        web.ProccesMessages();
        byte[] aydiobytes = micro.GetConvertBytes(3200);

        if (checkconnect)
        {
            if (aydiobytes != null && web.CheckConnectToServer())
            {
                web.SendAudioToServer(aydiobytes);
            }
            if (timeend > 0)
            {
                timeend -= Time.deltaTime;
                if (timeend < 0) timeend = 0;
                TimeSpan timemin = TimeSpan.FromSeconds(timeend);
                timetheendtext.text = timemin.ToString(@"mm\:ss");
            }
            else if (timeend == 0)
            {
                StopCall();
                ExitOnOff(false, true);
            }
        }
    }
    void OnServer()
    {
        MessageText messagefile = new MessageText { type = "file", text = file };

        web.SendTextToServer(JsonUtility.ToJson(messagefile));
        micro.StartMicro();
        checkconnect = true;

        User userdata = saveload.LoadUser();
        MessageText messageid = new MessageText { type = "id", text = userdata.user_id.ToString() };
        web.SendTextToServer(JsonUtility.ToJson(messageid));
    }

    void SendNameFile(string name)
    {
        file = name;
    }


    void HandleText(string text)
    {
        var data = JsonUtility.FromJson<MessageText>(text);
        if (data.type == "сброс")
        {
            sub.text = data.text;
            StopCall();
            ExitOnOff(false, true);
        }
        else if (data.type == "клиент" || data.type == "я")
        {
            sub.text = data.text;
        }
        else if (data.type == "total_succes")
        {
            callsuccestext.text = data.text;
        }

    }

    void ExitOnOff(bool exitcall, bool exit)
    {
        exitcallbutton.SetActive(exitcall);
        exitbutton.SetActive(exit);
    }

    void HandleEndCall()
    {
        StopCall();
        ExitOnOff(false, true);
    }


    void StopCall()
    {
        micro.StopMicro();
        web.CloseConnectToServer();
    }

    void OnDisable()
    {
        sub.text = "";
        callsuccestext.text = "";
        web.OnMessageReceveid -= HandleText;
        web.OnConnected -= OnServer;
        getscript.GetNameFile -= SendNameFile;
        endcall.OnCallEnded -= HandleEndCall;
        StopCall();
        checkconnect = false;
    }


    [System.Serializable]
    public class BaseMessage
    {
        public string type;
    }

    [System.Serializable]
    public class MessageText: BaseMessage
    {
        public string text;
    }
}
