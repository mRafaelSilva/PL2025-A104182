program QuadradoDeNumero;

var
  numero, resultado: integer;

begin
  writeln('Introduza um número inteiro:');
  readln(numero);
  resultado := numero * numero;
  writeln('O quadrado de ', numero, ' é: ', resultado);
end.
