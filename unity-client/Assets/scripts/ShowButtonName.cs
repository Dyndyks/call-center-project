using TMPro;
using UnityEngine;

public class ShowButtonName : MonoBehaviour
{
    public GameObject namebutton;
    public GameObject menubutton;
    public TMP_InputField inputname;


    private void OnEnable()
    {
        menubutton.SetActive(false);
        namebutton.SetActive(false);
    }


    public void OnTextChanged()
    {
        namebutton.SetActive(inputname.text.Length > 0);
    }
}
