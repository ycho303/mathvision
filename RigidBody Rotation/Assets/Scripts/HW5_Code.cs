using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HW5_Code : MonoBehaviour {
	public bool is_default = true;
	private Vector3 p1, p2, p3, p4, p5, p1p, p2p, p3p;
	
	// Use this for initialization
	void Start () {
		p1 = new Vector3(-0.500000f, 0.000000f, 2.121320f);
		p2 = new Vector3(0.500000f, 0.000000f, 2.121320f);
		p3 = new Vector3(0.500000f, -0.707107f, 2.828427f);

		p1p = new Vector3(1.363005f, -0.427130f, 2.339082f);
		p2p = new Vector3(1.748084f, 0.437983f, 2.017688f);
		p3p = new Vector3(2.636461f, 0.184843f, 2.400710f);

		if (is_default) {
			p4 = new Vector3(0.500000f, 0.707107f, 2.828427f);
			p5 = new Vector3(1.0f, 1.0f, 1.0f);
		}

		// R1
		Vector3 h = Vector3.Cross(p2-p1, p3-p1);
		Vector3 hp = Vector3.Cross(p2p-p1p, p3p-p1p);
		Vector3 u = Vector3.Cross(h, hp).normalized;

		float hhp_mag = h.magnitude * hp.magnitude;
		float r1_sine = Vector3.Cross(h,hp).magnitude / hhp_mag;
		float r1_cosine = Vector3.Dot(h,hp) / hhp_mag;
		Vector3[] r1 = rotation_matrix(u, r1_sine, r1_cosine);
		print("R1");
		print(r1[0].ToString("F10"));
		print(r1[1].ToString("F10"));
		print(r1[2].ToString("F10"));

		// R2
		Vector3 v = hp.normalized;
		Vector3[] p2p1 = new Vector3[1];
		p2p1[0] = p2-p1;
	
		float[,] tmp = matmul(r1, p2p1);
		Vector3 r1p2p1 = new Vector3(tmp[0,0], tmp[1,0], tmp[2,0]);

		float r2_mag = r1p2p1.magnitude * (p2p-p1p).magnitude;
		float r2_sine = Vector3.Cross(r1p2p1, p2p-p1p).magnitude / r2_mag;
		float r2_cosine = Vector3.Dot(r1p2p1, p2p-p1p) / r2_mag;

		Vector3[] r2 = v2v_3x3transpose(rotation_matrix(v, r2_sine, r2_cosine));
		print("R2");
		print(r2[0].ToString("F10"));
		print(r2[1].ToString("F10"));
		print(r2[2].ToString("F10"));

		Vector3 p4p = transform(r1, r2, p1, p1p, p4);
		print("p4':");
		print(p4p.ToString("F10"));

		Vector3 p5p = transform(r1, r2, p1, p1p, p5);
		print("p5':");
		print(p5p.ToString("F10"));
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	Vector3[] rotation_matrix(Vector3 u, float sine, float cosine) {
		Vector3[] array = new Vector3[3];

		array[0] = new Vector3(cosine + power(u.x) * (1-cosine),
							   u.x * u.y * (1-cosine) - u.z * sine,
							   u.x * u.z * (1-cosine) + u.y * sine);
		
		array[1] = new Vector3(u.y * u.x * (1-cosine) + u.z * sine,
							   cosine + power(u.y) * (1-cosine),
							   u.y * u.z * (1-cosine) - u.x * sine);

		array[2] = new Vector3(u.z * u.x * (1-cosine) - u.y * sine,
							   u.z * u.y * (1-cosine) + u.x * sine,
							   cosine + power(u.z) * (1-cosine));

		return array;
	}

	float power(float x) {
		return x * x;
	}

	float[,] matmul(Vector3[] u, Vector3[] v) {
		// Only computes 3x3 * 3xn 
		float[,] result = new float[u.Length, v.Length];
		float[,] u_t = _3x3transpose(u); // need transpose bc Vector3[] format

        for (int i = 0; i < 3; i++) { 
            for (int j = 0; j < v.Length; j++) { 
				result[i,j] = 0; 
                for (int k = 0; k < u.Length; k++) 
					result[i, j] += u_t[i, k] * get_element(v, k, j); 
            } 
        }
		return result;
	}

	float[,] _3x3transpose(Vector3[] source) {
		float[,] result = new float[source.Length, source.Length];
		for (int i = 0; i < source.Length; i++) { 
			for (int j = 0; j < source.Length; j++) { 
				result[j, i] = get_element(source, i, j);
			} 
		} 
		return result;
	}
	
	Vector3[] v2v_3x3transpose(Vector3[] source) {
		float[,] tmp = new float[source.Length, source.Length];
		for (int i = 0; i < source.Length; i++) { 
			for (int j = 0; j < source.Length; j++) { 
				tmp[j, i] = get_element(source, i, j);
			} 
		} 
		Vector3[] result = new Vector3[3];
		result[0] = new Vector3(tmp[0, 0], tmp[1, 0], tmp[2, 0]);
		result[1] = new Vector3(tmp[0, 1], tmp[1, 1], tmp[2, 1]);
		result[2] = new Vector3(tmp[0, 2], tmp[1, 2], tmp[2, 2]);

		return result;
	}

	float get_element(Vector3[] target, int i, int j) {
		if (i==0) return (float)target[j].x;
		else if (i==1) return (float)target[j].y;
		else if (i==2) return (float)target[j].z;
		else {
			System.ArgumentException argEx = new System.ArgumentException("Index out of range");
        	throw argEx;
		};
	}

	Vector3 transform(Vector3[] r1, Vector3[] r2, Vector3 p1, Vector3 p1p, Vector3 source) {
		Vector3[] sourcep1 = new Vector3[1];
		sourcep1[0] = source - p1;

		float[,] tmp = matmul(r1 , sourcep1);
		Vector3[] tmp_to_vector = new Vector3[1];
		tmp_to_vector[0] = new Vector3(tmp[0, 0], tmp[1, 0], tmp[2, 0]);

		tmp = matmul(r2 , tmp_to_vector);
		Vector3 target = new Vector3(tmp[0, 0], tmp[1, 0], tmp[2, 0]);
		return target + p1p;
	}

}
