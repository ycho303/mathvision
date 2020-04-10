using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class display_position : MonoBehaviour {

	public GameObject p1, p2, p3, p4, p5;
	public Text p1_text, p2_text, p3_text, p4_text, p5_text;
	public string transform_text;
	public bool is_source;

	// Use this for initialization
	void Start () {
		if (is_source) {
			p1.transform.position = new Vector3(-0.500000f, 0.000000f, 2.121320f);
			p2.transform.position = new Vector3(0.500000f, 0.000000f, 2.121320f);
			p3.transform.position = new Vector3(0.500000f, -0.707107f, 2.828427f);
			p4.transform.position = new Vector3(0.500000f, -0.707107f, 2.828427f);
			p5.transform.position = new Vector3(1.0f, 1.0f, 1.0f);
		} else {
			p1.transform.position = new Vector3(1.363005f, -0.427130f, 2.339082f);
			p2.transform.position = new Vector3(1.748084f, 0.437983f, 2.017688f);
			p3.transform.position = new Vector3(2.636461f, 0.184843f, 2.400710f);
			p4.transform.position = new Vector3(1.4981f, 0.8710f, 2.8837f);
			// p5.transform.position = new Vector3(0.0f, 0.0f, 0.0f);
		}
	}
	
	// Update is called once per frame
	void Update () {
		p1_text.text = $"P1{transform_text}: " + p1.transform.position.ToString("F6");
		p2_text.text = $"P2{transform_text}: " + p2.transform.position.ToString("F6");
		p3_text.text = $"P3{transform_text}: " + p3.transform.position.ToString("F6");
		p4_text.text = $"P4{transform_text}: " + p4.transform.position.ToString("F6");
		p5_text.text = $"P5{transform_text}: " + p5.transform.position.ToString("F6");
		// p1_text.text = $"P1{transform_text}: " + left_to_right_coordinate_text(p1);
		// p2_text.text = $"P2{transform_text}: " + left_to_right_coordinate_text(p2);
		// p3_text.text = $"P3{transform_text}: " + left_to_right_coordinate_text(p3);
		// p4_text.text = $"P4{transform_text}: " + left_to_right_coordinate_text(p4);
		// p5_text.text = $"P5{transform_text}: " + left_to_right_coordinate_text(p5);
	}

	// string left_to_right_coordinate_text (GameObject pos) {
	// 	// Change coordinate from left hand to right hand coordinate for display purposes.
	// 	return $"({pos.transform.position.x}, {pos.transform.position.y}, {pos.transform.position.z})";
	// }
}
