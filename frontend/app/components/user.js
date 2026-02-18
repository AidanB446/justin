import styles from './user.module.css';

export default function User(props) {
  return (
    <details className={styles.container}>
      <summary className={styles.header}>
        {props.username}
      </summary>
      <div className={styles.content}>
        <p>api key: {props.api_key}</p>
        <p>api secret: {props.api_secret}</p>
        <p>paper trading: {props.paper_trading}</p>
      </div>
    </details>
  );
}


