using System;
using UnityEngine;

public class Micro : MonoBehaviour
{
    private string devicename;
    private AudioClip clip;
    private int lastposition = 0;

    public void StartMicro()
    {
        devicename = Microphone.devices[0];
        clip = Microphone.Start(devicename, false, 120, 16000);
    }

    public byte[] GetConvertBytes(int num)
    {
        if (!Microphone.IsRecording(devicename)) return null;

        int currentposition = Microphone.GetPosition(devicename);
        int differenceposition = currentposition - lastposition;
        if (differenceposition >= num)
        {
            float[] chunk = new float[differenceposition];
            clip.GetData(chunk, lastposition);
            lastposition = currentposition;
            return ConvertToBytes(chunk);
        }
        return null;
    }

    byte[] ConvertToBytes(float[] chunk)
    {
        short[] intdata = new short[chunk.Length];
        for (int i = 0; i < intdata.Length; i++)
        {
            intdata[i] = (short)(chunk[i] * 32767);
        }
        byte[] bytesdata = new byte[intdata.Length * 2];
        Buffer.BlockCopy(intdata, 0, bytesdata, 0, bytesdata.Length);
        return bytesdata;
    }

    public void StopMicro()
    {
        if (Microphone.IsRecording(devicename))
        {
            Microphone.End(devicename);
        }
        lastposition = 0;
    }
}
