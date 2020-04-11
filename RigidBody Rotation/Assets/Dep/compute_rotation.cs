using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class compute_rotation : MonoBehaviour {
	public GameObject source, target;

	// Use this for initialization
	void Start () {
		Vector3 source_pos = source.transform.position;
	}
	
	// Update is called once per frame
	void Update () {
		Vector3 target_pos = target.transform.position;
	}
}
