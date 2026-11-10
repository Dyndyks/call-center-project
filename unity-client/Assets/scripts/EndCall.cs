using System;
using UnityEngine;


public class EndCall : MonoBehaviour
{
    public event Action OnCallEnded;
    public void ClickEndCall()
    {
        OnCallEnded?.Invoke();
    }
}
