using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class display_position : MonoBehaviour {

	public GameObject p1, p2, p3, p4, p5, p6;
	public Text p1_text, p2_text, p3_text, p4_text, p5_text, p6_text;
	public Text p1p_text, p2p_text, p3p_text, p4p_text, p5p_text, p6p_text;
	private Vector3 _p1, _p2, _p3, _p4, _p5, _p6;

	// Use this for initialization
	void Start () {
		// Earth
		_p1 = p1.transform.position;
		_p2 = p2.transform.position;
		_p3 = p3.transform.position;

		// Meteor
		_p4 = p4.transform.position;
		_p5 = p5.transform.position;
		_p6 = p6.transform.position;
	}
	
	// Update is called once per frame
	void Update () {
		p1_text.text = $"P1: {_p1.ToString("F4")}";
		p1p_text.text = $"P1': {p1.transform.position.ToString("F4")}";

		p2_text.text = $"P2: {_p2.ToString("F4")}";
		p2p_text.text = $"P2': {p2.transform.position.ToString("F4")}";

		p3_text.text = $"P3: {_p3.ToString("F4")}";
		p3p_text.text = $"P3': {p3.transform.position.ToString("F4")}";

		p4_text.text = $"P4: {_p4.ToString("F4")}";
		p4p_text.text = $"P4': {p4.transform.position.ToString("F4")}";

		p5_text.text = $"P5: {_p5.ToString("F4")}";
		p5p_text.text = $"P5': {p5.transform.position.ToString("F4")}";

		p6_text.text = $"P6: {_p6.ToString("F4")}";
		p6p_text.text = $"P6': {p6.transform.position.ToString("F4")}";
	}
}
