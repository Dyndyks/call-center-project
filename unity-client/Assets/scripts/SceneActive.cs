using UnityEngine;

public class SceneActive : MonoBehaviour
{
    public SaveLoad saveload;
    public GameObject setname;
    public GameObject menu;
    public GameObject scene;


    public void ShowSetName()
    {
        setname.SetActive(true);
        menu.SetActive(false);
        scene.SetActive(false);
    }

    public void ShowMenu()
    {
        setname.SetActive(false);
        menu.SetActive(true);
        scene.SetActive(false);
    }

    public void ShowScene()
    {
        setname.SetActive(false);
        menu.SetActive(false);
        scene.SetActive(true);
    }

    private void Start()
    {
        User userdata = saveload.LoadUser(); 
        if (userdata != null)
        {
            ShowMenu();
        }
        else
        {
            ShowSetName();
        }
    }
}
