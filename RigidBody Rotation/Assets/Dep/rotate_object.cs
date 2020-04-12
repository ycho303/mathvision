using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rotate_object : MonoBehaviour {
	public bool rotate_left = false;
    public int rotate_speed = 20;
	private Vector3 pos;
	// Use this for initialization
	void Start () {
		pos = transform.position;
	}
	
	// Update is called once per frame
	void Update () {
		if (rotate_left)
        transform.RotateAround(pos, Vector3.up, rotate_speed * Time.deltaTime);
        else 
        transform.RotateAround(pos, -Vector3.up, rotate_speed * Time.deltaTime);
	}
}
