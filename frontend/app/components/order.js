
import styles from "./order.module.css";

export default function Order(props) {

	const newArr = [
	  ...props.pipe.slice(0, 5),
	  ...props.pipe.slice(7)
	];

		


	return (
		<div className={styles.order}>
			<p>{newArr.join(" | ")}</p>
		</div>
	);
}

