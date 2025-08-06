import netherlandsRecruiter from './jeremy-akeze-doghouse-it-recruitment.jpg';
import * as S from './style';

const Recruiter = () => (
  <S.Container>
    <S.Thumbnail>
      <img
        alt="Jeremy Akeze - Doghouse IT Recruitment"
        src={netherlandsRecruiter}
      />
    </S.Thumbnail>
    <S.Description>
      <h4>
        Work in the Netherlands
        <S.Flag />
      </h4>
      <p>
      </p>
    </S.Description>
  </S.Container>
);

export default Recruiter;
