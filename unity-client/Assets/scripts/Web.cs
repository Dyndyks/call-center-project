using System;
using System.Threading.Tasks;
using UnityEngine;

public class Web : MonoBehaviour
{
    private NativeWebSocket.WebSocket ws;

    public event Action<string> OnMessageReceveid;
    public event Action OnConnected;
    public async Task ConnectToServer()
    {
        ws = new NativeWebSocket.WebSocket("ws://127.0.0.1:8000/dialog");

        ws.OnOpen += () => OnConnected?.Invoke();
        ws.OnError += (e) => Debug.Log($"ошибка: {e}");
        ws.OnClose += (e) => Debug.Log("отключился");

        ws.OnMessage += (bytes) =>
        {
            string text = System.Text.Encoding.UTF8.GetString(bytes);
            OnMessageReceveid?.Invoke(text);
        };
        await ws.Connect();
    }

    public void SendAudioToServer(byte[] aydiobytes)
    {
        if (CheckConnectToServer())
        {
            ws.Send(aydiobytes);
        }
    }

    public void SendTextToServer(string message)
    {
        if (CheckConnectToServer())
        {
            ws.SendText(message);
        }
    }

    public void CloseConnectToServer()
    {
        if (CheckConnectToServer())
        {
            ws.Close();
        }
    }


    public bool CheckConnectToServer()
    {
        if (ws != null && ws.State == NativeWebSocket.WebSocketState.Open)
        {
            return true;
        }
        return false;
    }

    public void ProccesMessages()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
        ws?.DispatchMessageQueue();
        #endif
    }
}
